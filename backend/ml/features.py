import pandas as pd

from ml.type_chart import type_chart

STATS = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
FEATURES = (
    [f"{s}_1" for s in STATS]
    + [f"{s}_2" for s in STATS]
    + ["type_advantage_1", "type_advantage_2"]
)


def type_advantage(attacker_types, defender_types) -> float:
    """Multiplicador total de efetividade dos tipos do atacante sobre os do defensor."""
    multiplier = 1.0
    for atk in attacker_types:
        if pd.notna(atk):
            for dfn in defender_types:
                if pd.notna(dfn):
                    multiplier *= type_chart.get(atk.lower(), {}).get(dfn.lower(), 1.0)
    return multiplier


def types_of(pokemon) -> list:
    return [pokemon["Type 1"], pokemon["Type 2"]]
