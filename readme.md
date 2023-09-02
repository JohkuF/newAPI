# NewAPI - A Python API Framework

NewAPI is a lightweight Python API framework that simplifies the process of building and deploying RESTful APIs using Python sockets.

## Features

- Built on top of Python sockets for low-level network communication.
- Define API endpoints using decorators.
- Easily validate and serialize data using Pydantic models.

## Getting Started

To get started with NewAPI, you can install it using pip:

```bash
pip install newapi
```

## Example Usage
```python
from pydantic import BaseModel
from newapi import NewAPI

class Info(BaseModel):
    name: str
    age: int | None = None

app = NewAPI("127.0.0.1", 8097)

@app.get("/hello")
def hello(name: str, age: int | None = None):
    return {"name": name, "age": age}

@app.post("/hello")
def post_hello(name: str, age: int | None = None):
    return Info.model_validate({"name": name, "age": age}).model_dump(exclude_none=True)

if __name__ == "__main__":
    app.start()
```

## Supported HTTP Methods

NewAPI currently supports the following HTTP methods:

- **GET**: Used for retrieving data from the server.
- **POST**: Used for creating or updating data on the server.

Additional HTTP methods such as PUT, DELETE, or PATCH may be considered for future updates to the framework.

If you require support for other HTTP methods, you may need to consider alternative frameworks or implement custom functionality.


## In Todo

- Currently working on making the code asynchronous
