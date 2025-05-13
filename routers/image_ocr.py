from fastapi import APIRouter, UploadFile, File
import pytesseract
from PIL import Image
import io

router = APIRouter()

@router.post("/extract-text")
def extract_text(file: UploadFile = File(...)):
    image_bytes = io.BytesIO(file.file.read())
    image = Image.open(image_bytes)
    text = pytesseract.image_to_string(image)
    return {"text": text.strip()}
	