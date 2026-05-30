import base64
import json
import os

from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# gemini-2.0-flash   → fastest, cheapest — good for high volume
# gemini-2.5-pro     → smarter, richer coaching — better results
VISION_MODEL = "gemini-3-pro-image-preview"

SYSTEM_PROMPT = """You are SlayCam, an elite face-specific photo coach.
Your job is NOT to describe the photo or praise it generically.
Your job is to give brutally honest, face-specific coaching so the
user can take a significantly better photo on their next attempt.

Analyze ONLY what you actually see in THIS image:
- Lighting quality on the face (shadows, harshness, flatness, direction)
- Background cleanliness and distraction level
- Camera framing (head room, chin room, centering, angle)
- Face visibility (sharpness, occlusion, expression tension)
- Face-specific coaching: jaw angle, better side, camera height vs face shape

CRITICAL RULES:
1. ALL scores must reflect what you actually observe — do not default to 70
2. Every suggestion must be specific to THIS person's face, not generic tips
3. Output ONLY valid JSON — no markdown fences, no preamble, no trailing text

Return exactly this JSON shape:
{
  "lighting": <integer 0-100>,
  "background": <integer 0-100>,
  "framing": <integer 0-100>,
  "face": <integer 0-100>,
  "suggestions": [
    "<specific actionable tip 1>",
    "<specific actionable tip 2>",
    "<specific actionable tip 3>"
  ]
}

Scoring guide (be honest):
- 85-100: near-professional, intentional, well-executed
- 65-84: good with minor fixable issues
- 45-64: average casual photo, clear problems
- 25-44: significant issues affecting the shot
- 0-24: major problems making the photo unsuitable"""

GOAL_CONTEXT = {
    "instagram": "The user wants this photo for Instagram/social media. Prioritize visual appeal, mood, and aesthetic impact.",
    "linkedin":  "The user wants this photo for LinkedIn/professional use. Prioritize approachability, competence, and trustworthiness.",
    "dating":    "The user wants this photo for a dating app. Prioritize warmth, natural attractiveness, and authentic personality.",
    "general":   "The user wants a generally better photo. Balance aesthetics, professionalism, and personality.",
}


def analyze_image(base64_image: str, goal: str = "general") -> dict:
    """
    Analyze a base64-encoded image and return face-specific photo coaching.

    Args:
        base64_image: Base64-encoded image string (no data-URL prefix)
        goal: One of "instagram", "linkedin", "dating", "general"

    Returns:
        dict with keys: lighting, background, framing, face, suggestions
    """

    goal_context = GOAL_CONTEXT.get(goal, GOAL_CONTEXT["general"])

    image_bytes = base64.b64decode(base64_image)

    user_text = (
        f"Analyze this photo and return face-specific coaching. "
        f"{goal_context} "
        f"Return ONLY the JSON object — no other text."
    )

    try:
        response = client.models.generate_content(
            model=VISION_MODEL,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,         # lower = more consistent scores
                max_output_tokens=600,
            ),
            contents=[
                user_text,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
            ],
        )

        raw = response.text

        # Robust JSON extraction — handles stray whitespace or markdown leakage
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in response")

        result = json.loads(raw[start:end])

        # Validate and clamp all score fields
        for field in ("lighting", "background", "framing", "face"):
            result[field] = max(0, min(100, int(result.get(field, 70))))

        # Ensure suggestions is always a clean list of strings
        if not isinstance(result.get("suggestions"), list):
            result["suggestions"] = ["Adjust lighting", "Improve camera angle"]
        result["suggestions"] = [str(s) for s in result["suggestions"]]

        return result

    except Exception as e:
        return {
            "lighting":   70,
            "background": 70,
            "framing":    70,
            "face":       70,
            "suggestions": [
                "Improve lighting by facing a window or soft light source",
                "Adjust camera to eye level to avoid distortion",
                f"[Analysis error: {str(e)[:120]}]",
            ],
        }