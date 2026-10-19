from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
POKEMON_CSV = DATA_DIR / "pokemon.csv"
COMBATS_CSV = DATA_DIR / "combats.csv"


def data_loading(pokemon_path=POKEMON_CSV, batalha_path=COMBATS_CSV):
    """Carrega os CSVs de pokémon e de combates."""
    return pd.read_csv(pokemon_path), pd.read_csv(batalha_path)
