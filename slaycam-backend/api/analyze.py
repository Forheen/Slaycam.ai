from fastapi import FastAPI, UploadFile, File
import base64

from services.gemini_service import analyze_image
from utils.scoring import calculate_score

app = FastAPI()

@app.get("/")
def home():

    return {"status":"running"}

@app.post("/api/analyze")

async def analyze(file: UploadFile = File(...)):

    contents = await file.read()

    base64_image = base64.b64encode(contents).decode()

    gemini_result = analyze_image(base64_image)

    score = calculate_score(gemini_result)

    return {

        "success":True,
        "score":score,
        "analysis":gemini_result

    }