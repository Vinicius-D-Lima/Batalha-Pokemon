from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from predicoes.prediction import PokemonNaoEncontrado, prever_ganhador

app = FastAPI(title="Batalha Pokémon", description="Previsão de vencedor de batalhas Pokémon com ML")

# Permite que o app web (Expo) consuma a API.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class PokemonRequest(BaseModel):
    nome1: str
    nome2: str


class PrevisaoResponse(BaseModel):
    vencedor: str
    confianca: float


@app.get("/")
def home():
    return {"mensagem": "API de IA Pokémon online!"}


@app.post("/prever", response_model=PrevisaoResponse)
def prever_batalha(data: PokemonRequest):
    try:
        return prever_ganhador(data.nome1, data.nome2)
    except PokemonNaoEncontrado as erro:
        raise HTTPException(status_code=404, detail=str(erro))
