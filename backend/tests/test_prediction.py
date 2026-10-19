import pytest
from fastapi.testclient import TestClient

from app.main import app
from ml.features import type_advantage
from ml.predict import PokemonNotFound, Predictor


@pytest.fixture(scope="module")
def predictor():
    return Predictor()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:  # o `with` dispara o lifespan que carrega o modelo
        yield c


def test_type_advantage():
    assert type_advantage(["Fire"], ["Grass"]) == 2.0
    assert type_advantage(["Water"], ["Dragon"]) == 0.5
    assert type_advantage(["Normal"], ["Ghost"]) == 0.0
    assert type_advantage(["Fire", "None"], ["None"]) == 1.0


def test_prediction_does_not_depend_on_order(predictor):
    a = predictor.predict_winner("Charizard", "Bulbasaur")
    b = predictor.predict_winner("Bulbasaur", "Charizard")
    assert a["vencedor"] == b["vencedor"]
    assert a["confianca"] == pytest.approx(b["confianca"], abs=1e-3)


def test_unknown_pokemon(predictor):
    with pytest.raises(PokemonNotFound):
        predictor.predict_winner("Naoexiste", "Pikachu")


def test_api_predict(client):
    resp = client.post("/prever", json={"nome1": "Pikachu", "nome2": "Snorlax"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["vencedor"] in ("Pikachu", "Snorlax")
    assert 0.5 <= body["confianca"] <= 1.0


def test_api_invalid_name_returns_404(client):
    resp = client.post("/prever", json={"nome1": "xxx", "nome2": "Pikachu"})
    assert resp.status_code == 404
