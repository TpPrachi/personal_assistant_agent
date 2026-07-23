import os

from dotenv import load_dotenv
from fastapi import FastAPI
from anthropic import Anthropic
from ollama import chat

load_dotenv()

app = FastAPI()

ENV = os.getenv("APP_ENV", "development")

client = None
if ENV == "production":
    client = Anthropic()


@app.get("/")
def root():
    return {"message": "Personal Agent is running!"}


@app.post("/ask")
def ask(body: dict):
    question = body["question"]

    if ENV == "production":
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": question}
            ],
        )

        answer = response.content[0].text

    else:
        response = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": question,
                }
            ],
        )

        answer = response["message"]["content"]

    return {"answer": answer}
