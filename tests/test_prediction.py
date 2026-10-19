import pytest
from fastapi.testclient import TestClient

from main import app
from modelo_treinado.model import calc_total_vantagem
from predicoes.prediction import PokemonNaoEncontrado, prever_ganhador

client = TestClient(app)


def test_vantagem_de_tipos():
    assert calc_total_vantagem(["Fire"], ["Grass"]) == 2.0
    assert calc_total_vantagem(["Water"], ["Dragon"]) == 0.5
    assert calc_total_vantagem(["Normal"], ["Ghost"]) == 0.0
    assert calc_total_vantagem(["Fire", "None"], ["None"]) == 1.0


def test_previsao_nao_depende_da_ordem():
    a = prever_ganhador("Charizard", "Bulbasaur")
    b = prever_ganhador("Bulbasaur", "Charizard")
    assert a["vencedor"] == b["vencedor"]
    assert a["confianca"] == pytest.approx(b["confianca"], abs=1e-3)


def test_pokemon_inexistente():
    with pytest.raises(PokemonNaoEncontrado):
        prever_ganhador("Naoexiste", "Pikachu")


def test_api_prever():
    resp = client.post("/prever", json={"nome1": "Pikachu", "nome2": "Snorlax"})
    assert resp.status_code == 200
    corpo = resp.json()
    assert corpo["vencedor"] in ("Pikachu", "Snorlax")
    assert 0.5 <= corpo["confianca"] <= 1.0


def test_api_nome_invalido_retorna_404():
    resp = client.post("/prever", json={"nome1": "xxx", "nome2": "Pikachu"})
    assert resp.status_code == 404
