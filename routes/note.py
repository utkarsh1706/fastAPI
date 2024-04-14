from fastapi import APIRouter, Request
from models.note import Note
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.db import conn
from schemas.note import noteEntity, notesEntity

note = APIRouter()

templates = Jinja2Templates(directory="templates")
db = conn["Notes"]
collection = db["Notes"]  

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = collection.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

@note.post("/")
async def create_item(request: Request):
    form  = await request.form()
    formDict = dict(form)
    formDict['important'] = True if formDict.get("important")=="on" else False
    note = collection.insert_one(formDict)
    return {"Success": True}