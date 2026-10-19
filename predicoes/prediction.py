from functools import lru_cache

import pandas as pd

from modelo_treinado.model import FEATURES, STATS, calc_total_vantagem, load_model
from utils.pre_process_data import pré_processamento


class PokemonNaoEncontrado(ValueError):
    pass


@lru_cache(maxsize=1)
def _pokemon():
    return pré_processamento()[0]


@lru_cache(maxsize=1)
def _model():
    return load_model()


def _buscar(nome):
    resultado = _pokemon()[lambda df: df["Name"] == nome.strip().lower()]
    if resultado.empty:
        raise PokemonNaoEncontrado(f"Pokémon não encontrado: '{nome}'. Verifique a grafia.")
    return resultado.iloc[0]


def _prob_primeiro_vencer(a, b):
    tipos_a = [a["Type 1"], a["Type 2"]]
    tipos_b = [b["Type 1"], b["Type 2"]]
    linha = [a[s] for s in STATS] + [b[s] for s in STATS]
    linha += [calc_total_vantagem(tipos_a, tipos_b), calc_total_vantagem(tipos_b, tipos_a)]
    return _model().predict_proba(pd.DataFrame([linha], columns=FEATURES))[0][1]


def prever_ganhador(nome1, nome2):
    """Prevê o vencedor. A previsão é feita nas duas ordens e a média é usada,
    para que a ordem dos nomes não influencie o resultado."""
    p1, p2 = _buscar(nome1), _buscar(nome2)

    prob_1 = (_prob_primeiro_vencer(p1, p2) + (1 - _prob_primeiro_vencer(p2, p1))) / 2
    if prob_1 >= 0.5:
        vencedor, confianca = p1["Name"].title(), prob_1
    else:
        vencedor, confianca = p2["Name"].title(), 1 - prob_1

    return {"vencedor": vencedor, "confianca": round(float(confianca), 4)}
