from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from auth import router as auth_router
from config import *


app = FastAPI()
app.include_router(auth_router)
msg = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key="a_long_random_secret_key_here",
    same_site="lax",
    https_only=True,
)

class Message(BaseModel):
    text: str

@app.get("/")
def root():
    return {f"client" : {GOOGLE_CLIENT_ID}, f"secret" : {GOOGLE_CLIENT_SECRET}, f"redirect" : {REDIRECT_URL}}

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
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )


if __name__ == "__main__":
    run()