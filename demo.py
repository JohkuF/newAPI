import json
import logging
import uvicorn
from pprint import pprint

from pydantic import BaseModel
from newapi import NewAPI, HTMLResponse

class Info(BaseModel):
    name: str
    age: int | None = None

app = NewAPI("127.0.0.1", 8098)

@app.get("/")
def main():
    return HTMLResponse('<h1>HELLO</h1>')

@app.get("/hello")
def hello(name: str, age: int | None = None):
    return {'name': name, 'age': age}

@app.post("/hello")
def post_hello(name: str, age: int | None = None):
    return Info.model_validate({"name": name, "age": age}).model_dump(exclude_none=True)

"""

async def asgi_app(scope, receive, send):
    assert scope['type'] == 'http'

    while True:
        message = await receive()
        if message['type'] == 'http.disconnect':
            break
        if message['type'] == 'http.request':
            pprint(scope)
            http_method = scope.get('method', b'').decode('utf-8')
            http_path = scope.get('path', b'').decode('utf-8')
            headers = scope.get('headers', [])

            print(http_method, http_path, headers)
"""



if __name__ == "__main__":
    pass
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format=json.dumps({'timestamp': '%(asctime)s', 'level': '%(levelname)s', 'message': '%(message)s'}),
        handlers=[logging.StreamHandler()]
    )
    """
    #config = uvicorn.Config('demo:app', port=8098, log_level='debug')
    uvicorn.run('demo:asgi_app', port=8098, reload=True)
