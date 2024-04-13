from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Union
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

conn = MongoClient(os.getenv("DATABASE_URL"))
db = conn["Notes"]
collection = db["Notes"]  

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = collection.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "note": doc["note"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})
