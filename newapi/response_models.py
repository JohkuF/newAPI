import json


def JSONResponse(content):
    content = json.dumps(content, indent=0)
    http_response = f"HTTP/1.1 200 OK\r\n"
    http_response += f"Content-Type: application/json\r\n"
    http_response += f"Content-Length: {len(content)}\r\n\r\n"
    http_response += content
    return http_response


def HTMLResponse(content):
    # TODO
    pass
