import base64
import json
import os

from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

TEXT_MODEL="gemini-3-pro-image-preview"

def analyze_image(base64_image):

    prompt = """
You are an AI camera coach.

Analyze this creator image.

Evaluate:

Lighting quality (0-100)
Background cleanliness (0-100)
Camera framing (0-100)
Face visibility (0-100)

Return STRICT JSON:

{
"lighting": number,
"background": number,
"framing": number,
"face": number,
"suggestions":[]
}

Suggestions must be actionable camera improvements.
"""

    image_bytes = base64.b64decode(base64_image)

    response = client.models.generate_content(

        model=TEXT_MODEL,

        contents=[

            prompt,

            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )

        ]

    )

    text=response.text

    try:

        start=text.find("{")

        end=text.rfind("}")+1

        clean=text[start:end]

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