import os
from fastapi import UploadFile
from PyPDF2 import PdfReader
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")

def save_file(file: UploadFile):
    if not os.path.exists(UPLOAD_DIR):
        os.mkdir(UPLOAD_DIR)
    
    file_ext = file.filename.split(".")[-1]
    unique_name = f"{uuid4()}.{file_ext}"

    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path, file_ext

def detect_file_type(file_ext: str):
    file_ext = file_ext.lower()

    if file_ext == "pdf":
        return "pdf"
    elif file_ext in ["jpeg", "png", "jpg"]:
        return "image"
    
    return "unsupported" 

def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        content = page.extract_text()

        if content:
            text += content + "\n"

    return text