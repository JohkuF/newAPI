import json
import logging

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
    logging.basicConfig(
        level=logging.DEBUG,
        format=json.dumps({'timestamp': '%(asctime)s', 'level': '%(levelname)s', 'message': '%(message)s'}),
        #format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    app.start()
