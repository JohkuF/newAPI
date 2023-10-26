import uvicorn
from pprint import pprint

from demo import app

async def asgi_app(scope, receive, send):
    assert scope['type'] == 'http'
    
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'text/html')],
    })

    while True:
        message = await receive()
        if message['type'] == 'http.disconnect':
            break
        if message['type'] == 'http.request':
            response = await app._handle_request(scope, message)
            
            await send(
                {
                    'type': 'http.response.body',
                    'body': response.encode('utf-8'),
                    'headers': [(b'content-type', b'application/json')]
                }
            )

if __name__ == '__main__':
    uvicorn.run('run:asgi_app', port=8098, reload=True)
