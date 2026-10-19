from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import PredictionResponse, PredictRequest
from ml.predict import PokemonNotFound, Predictor


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.predictor = Predictor()
    yield


app = FastAPI(
    title="Batalha Pokémon",
    description="Previsão de vencedor de batalhas Pokémon com ML",
    lifespan=lifespan,
)

# Permite que o app web (Expo) consuma a API.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def home():
    return {"mensagem": "API de IA Pokémon online!"}


@app.post("/prever", response_model=PredictionResponse)
def predict_battle(data: PredictRequest, request: Request):
    try:
        return request.app.state.predictor.predict_winner(data.nome1, data.nome2)
    except PokemonNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))
