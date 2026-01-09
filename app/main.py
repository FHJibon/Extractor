from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.services.parsing import extract_text_from_file, parse_with_openai
from app.schema import ExtractResponse, Invoice

app = FastAPI(title="Invoice Parsing API")

@app.post("/extract", response_model=ExtractResponse, tags=["Upload"])
async def extract_invoice(
    user_ID: str = Form(None),
    userId: str = Form(None),
    file: UploadFile = File(...)
):
    if not user_ID and userId:
        user_ID = userId
    if not user_ID:
        raise HTTPException(status_code=422, detail="Missing form field 'user_ID' (or legacy 'userId')")
    raw_text = await extract_text_from_file(file)

    invoice_data = await parse_with_openai(raw_text)

    invoice = Invoice(**invoice_data)

    return ExtractResponse(
        user_ID=user_ID,
        invoice=invoice
    )

@app.get("/")
async def root():
    return {"message": "Invoice Parsing API is running."}