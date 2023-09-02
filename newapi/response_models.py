import json

class Response:
    def dumps(self):
        return self.response

class JSONResponse(Response):
    def __init__(self, content) -> None:
        content = json.dumps(content, indent=0)
        response = f"HTTP/1.1 200 OK\r\n"
        response += f"Content-Type: application/json\r\n"
        response += f"Content-Length: {len(content)}\r\n\r\n"
        response += content
        self.response = response
    
class HTMLResponse(Response):
    def __init__(self, content) -> None:
        response = f'HTTP/1.1 200 OK\r\n'
        response += f'Content-Type: text/html\r\n'
        response += f'Content-Length: {len(content)}\r\n\r\n'
        response += content
        self.response = response
