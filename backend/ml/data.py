from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_pokemon() -> pd.DataFrame:
    """Carrega e limpa os pokémon: Type 2 vazio vira 'None' e nomes ficam em minúsculas."""
    df = pd.read_csv(DATA_DIR / "pokemon.csv")
    df["Type 2"] = df["Type 2"].fillna("None")
    df["Name"] = df["Name"].str.lower()
    return df.rename(columns={"#": "id"})


def load_battles() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "combats.csv")
