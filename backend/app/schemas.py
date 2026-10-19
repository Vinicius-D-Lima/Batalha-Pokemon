from pydantic import BaseModel


class PredictRequest(BaseModel):
    nome1: str
    nome2: str


class PredictionResponse(BaseModel):
    vencedor: str
    confianca: float
