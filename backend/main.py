from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()
msg = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    text: str


@app.get("/read")
def read_message():
    if not msg:
        return {"message": None}

    return {"message": msg[-1]}


@app.post("/send")
def send_message(message: Message):
    msg.append(message.text)

    return {
        "status": "sent",
        "message": message.text
    }


@app.get("/read/all")
def read_all():
    return msg


def run():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080
    )


if __name__ == "__main__":
    run()