import json
import socket
import inspect
import _thread
from pydantic import create_model, ValidationError, ConfigDict

from .router import Router
from .response_models import JSONResponse


class NewAPI(Router):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            try:
                client_socket, client_address = server_socket.accept()
                _thread.start_new_thread(self._handle_client, (client_socket,))

            except KeyboardInterrupt:
                print("Received KeyboardInterrupt. Shutting down server gracefully.")
                server_socket.shutdown(socket.SHUT_RDWR)
                server_socket.close()
                break  # Exit the loop

            except Exception as e:
                print(e)

    def _handle_client(self, client_socket: socket.socket):
        # Receive the header
        buffer: bytes = b""
        while True:
            data = client_socket.recv(128)
            if not data:
                break

            buffer += data
            if b"\r\n\r\n" in buffer:
                header, body = buffer.split(b"\r\n\r\n")
                break

        header = header.decode("utf-8")

        if header[:4] == "POST":
            # Receive rest of body
            content_lenght = int(header.split("Content-Length: ")[1].split(",")[0])

            body += client_socket.recv(content_lenght - len(body))

            body = json.loads(body.decode("utf-8"))

            response = self.handle_request(header, body)
            client_socket.sendall(response.encode("utf-8"))

        elif header[:3] == "GET":
            response = self.handle_request(header)
            client_socket.sendall(response.encode("utf-8"))

        else:
            response = "Invalid method or something idk"
            client_socket.sendall(response.encode("utf-8"))

        client_socket.close()

    def handle_request(self, header: str, body: dict | None = None):
        method, path, query_args = self.parse_request(header)
        handler = self.routes.get((method, path))

        if handler:
            if method == "GET":
                response = self._make_response(handler, query_args)

                if not callable(response):
                    return JSONResponse(response)
                return response

            elif body and method == "POST":
                response = self._make_response(handler, body)

                if not callable(response):
                    return JSONResponse(response)
                return response

        return "HTTP/1.1 404 Not Found\r\n\r\nRoute not found or invalid method"

    def parse_request(self, request_data: str):
        lines = request_data.strip().split("\r\n")

        method, full_path, _ = lines[0].split(" ")

        # Split the full path into path and query string
        if "?" in full_path:
            path, query_string = full_path.split("?")

            query_args = query_string.split("&")

            if len(query_args[-1]) == 0:
                query_args.pop()

        else:
            path = full_path
            query_args = []

        return method, path, self.query_args_to_dict(query_args)

    def _make_response(self, handler, data):
        Model = self.create_model_from_function(handler)
        # TODO raise error on missing value
        try:
            valid_args = Model.model_validate(data)
            return handler(**valid_args.model_dump())
        except ValidationError as e:
            return e.json()

    @staticmethod
    def query_args_to_dict(query_args: list[str]):
        args = {}
        for arg in query_args:
            key, value = arg.split("=")
            args[key] = value

        return args

    @staticmethod
    def create_model_from_function(handler):
        params = inspect.signature(handler).parameters
        fields = {}

        for param_name, param in params.items():
            param_type = (
                param.annotation if param.annotation != inspect.Parameter.empty else str
            )
            fields[param_name] = (param_type, param.default)

        dynamic_model = create_model(
            handler.__name__, **fields, __config__=ConfigDict(extra="forbid")
        )

        return dynamic_model
