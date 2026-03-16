import google.generativeai as genai
import os
import json

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.0-flash-preview-image-generation"
)

def analyze_image(base64_image):

    prompt = """

You are an AI camera coach for creators.

Analyze this image for content quality.

Evaluate:

Lighting quality (0-100)
Background cleanliness (0-100)
Camera framing (0-100)
Face visibility (0-100)

Return ONLY JSON:

{
"lighting": number,
"background": number,
"framing": number,
"face": number,
"suggestions":[]
}

Suggestions must be short actionable camera improvements.

"""

    response = model.generate_content([

        prompt,

        {
            "mime_type":"image/jpeg",
            "data":base64_image
        }

    ])

    text = response.text

    try:

        start = text.find("{")

        end = text.rfind("}")+1

        clean = text[start:end]

        return json.loads(clean)

    except:

        return {

            "lighting":70,

            "background":70,

            "framing":70,

            "face":70,

            "suggestions":[
                "Improve lighting",
                "Adjust camera angle"
            ]

        }