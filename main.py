from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from store_to_MongoDB import BankInfoStorage
from retrieve_from_mongoDB import BankInfoRetrieval
from fraud_detector import *
import tempfile
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.file.read())
        temp_pdf_path = temp_file.name

    storage = BankInfoStorage()
    storage.store_info(temp_pdf_path)
    retriever = BankInfoRetrieval()
    latest_data = retriever.retrieve_latest_info()
    transactions = find_transactions(json.dumps(latest_data, indent=4))
    insights = find_insights(transactions)
    fraud_detection_result = detect_fraud_all_transactions(transactions)

    return templates.TemplateResponse("results.html", {
        "request": request,
        "insights": insights,
        "fraud_detection_result": fraud_detection_result
    })