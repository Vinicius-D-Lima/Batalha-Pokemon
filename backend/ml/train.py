"""Treino do modelo. Rode a partir de backend/ com: python -m ml.train"""
from pathlib import Path

import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler

from ml.data import load_battles, load_pokemon
from ml.features import FEATURES, type_advantage, types_of

MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"


def build_dataset():
    pokemon, battles = load_pokemon(), load_battles()

    poke1 = pokemon.add_suffix("_1").rename(columns={"id_1": "First_pokemon"})
    poke2 = pokemon.add_suffix("_2").rename(columns={"id_2": "Second_pokemon"})
    df = battles.merge(poke1, on="First_pokemon").merge(poke2, on="Second_pokemon")

    df["first_won"] = (df["Winner"] == df["First_pokemon"]).astype(int)
    df["type_advantage_1"] = df.apply(
        lambda r: type_advantage([r["Type 1_1"], r["Type 2_1"]], [r["Type 1_2"], r["Type 2_2"]]), axis=1
    )
    df["type_advantage_2"] = df.apply(
        lambda r: type_advantage([r["Type 1_2"], r["Type 2_2"]], [r["Type 1_1"], r["Type 2_1"]]), axis=1
    )
    return df


def train(save=True):
    """Treina o pipeline (scaler + modelo), avalia no conjunto de teste e salva em disco."""
    df = build_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        df[FEATURES], df["first_won"], test_size=0.2, random_state=42
    )

    # O scaler faz parte do pipeline, então a previsão aplica a mesma normalização do treino.
    model = make_pipeline(
        MinMaxScaler(),
        GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42),
    )
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Acurácia no conjunto de teste: {accuracy:.2%}")

    if save:
        joblib.dump(model, MODEL_PATH)
        print(f"Modelo salvo em {MODEL_PATH}")
    return model, accuracy


def load_model():
    """Carrega o modelo salvo; se ainda não existir, treina e salva."""
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return train()[0]


if __name__ == "__main__":
    train()
