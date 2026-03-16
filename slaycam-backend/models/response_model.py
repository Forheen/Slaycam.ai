from pydantic import BaseModel

class AnalysisResponse(BaseModel):

    success: bool

    score: int

    analysis: dict