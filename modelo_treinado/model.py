"""Treino do modelo. Rode com: python -m modelo_treinado.model"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler

from predicoes.type_chart import type_chart
from utils.pre_process_data import pré_processamento

MODEL_PATH = Path(__file__).resolve().parent / "modelo_pokemon.pkl"

STATS = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
FEATURES = (
    [f"{s}_1" for s in STATS]
    + [f"{s}_2" for s in STATS]
    + ["type_advantage_1", "type_advantage_2"]
)


def calc_total_vantagem(tipo_atacante, tipo_defensor):
    """Multiplicador total de efetividade dos tipos do atacante sobre os do defensor."""
    multiplier = 1.0
    for atk_type in tipo_atacante:
        if pd.notna(atk_type):
            for def_type in tipo_defensor:
                if pd.notna(def_type):
                    multiplier *= type_chart.get(atk_type.lower(), {}).get(def_type.lower(), 1.0)
    return multiplier


def montar_dataset():
    pokemon, batalha = pré_processamento()

    poke1 = pokemon.add_suffix("_1").rename(columns={"id_1": "First_pokemon"})
    poke2 = pokemon.add_suffix("_2").rename(columns={"id_2": "Second_pokemon"})
    df = batalha.merge(poke1, on="First_pokemon").merge(poke2, on="Second_pokemon")

    df["ganhador_label"] = (df["Winner"] == df["First_pokemon"]).astype(int)
    df["type_advantage_1"] = df.apply(
        lambda r: calc_total_vantagem([r["Type 1_1"], r["Type 2_1"]], [r["Type 1_2"], r["Type 2_2"]]),
        axis=1,
    )
    df["type_advantage_2"] = df.apply(
        lambda r: calc_total_vantagem([r["Type 1_2"], r["Type 2_2"]], [r["Type 1_1"], r["Type 2_1"]]),
        axis=1,
    )
    return df


def train(salvar=True):
    """Treina o pipeline (scaler + modelo), avalia no conjunto de teste e salva em disco."""
    df = montar_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        df[FEATURES], df["ganhador_label"], test_size=0.2, random_state=42
    )

    # O scaler faz parte do pipeline, então a previsão aplica a mesma normalização do treino.
    model = make_pipeline(
        MinMaxScaler(),
        GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42),
    )
    model.fit(X_train, y_train)

    acuracia = accuracy_score(y_test, model.predict(X_test))
    print(f"Acurácia no conjunto de teste: {acuracia:.2%}")

    if salvar:
        joblib.dump(model, MODEL_PATH)
        print(f"Modelo salvo em {MODEL_PATH}")
    return model, acuracia


def load_model():
    """Carrega o modelo salvo; se ainda não existir, treina e salva."""
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return train()[0]


if __name__ == "__main__":
    train()
