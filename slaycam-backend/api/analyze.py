from fastapi import FastAPI, UploadFile, File
import base64

from services.gemini_service import analyze_image
from utils.scoring import calculate_score
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(

CORSMiddleware,

allow_origins=["*"],

allow_methods=["*"],

allow_headers=["*"]

)
@app.get("/")
def root():
    return {"status":"SlayCam backend running"}

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):

    contents = await file.read()

    base64_image = base64.b64encode(contents).decode()

    result = analyze_image(base64_image)

    score = calculate_score(result)

    return {
        "success": True,
        "score": score,
        "analysis": result
    }