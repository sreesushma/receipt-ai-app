from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import os

from backend.ocr_engine import extract_text  # adjust folder if needed
from backend.excel_manager import save_expense
from backend.parser import parse_receipt      # your parser

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="backend/templates")

UPLOAD_PATH = "temp.jpg"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    lines = extract_text(UPLOAD_PATH)
    data = parse_receipt(lines)

    # Save to Excel
    save_expense(data)

    os.remove(UPLOAD_PATH)
    return data

@app.get("/download")
def download_file():
    if os.path.exists("expenses.xlsx"):
        return FileResponse("expenses.xlsx", filename="expenses.xlsx")
    return {"error": "No expense file found"}