import pandas as pd

from ml.data import load_pokemon
from ml.features import FEATURES, STATS, type_advantage, types_of
from ml.train import load_model


class PokemonNotFound(ValueError):
    pass


class Predictor:
    """Guarda o modelo e a tabela de pokémon em memória."""

    def __init__(self, model=None, pokemon=None):
        self.model = model if model is not None else load_model()
        self.pokemon = pokemon if pokemon is not None else load_pokemon()

    def _find(self, name):
        found = self.pokemon[self.pokemon["Name"] == name.strip().lower()]
        if found.empty:
            raise PokemonNotFound(f"Pokémon não encontrado: '{name}'. Verifique a grafia.")
        return found.iloc[0]

    def _first_wins_probability(self, a, b):
        row = [a[s] for s in STATS] + [b[s] for s in STATS]
        row += [type_advantage(types_of(a), types_of(b)), type_advantage(types_of(b), types_of(a))]
        return self.model.predict_proba(pd.DataFrame([row], columns=FEATURES))[0][1]

    def predict_winner(self, name1, name2):
        """Prevê o vencedor. A previsão é feita nas duas ordens e a média é usada,
        para que a ordem dos nomes não influencie o resultado."""
        p1, p2 = self._find(name1), self._find(name2)

        prob_1 = (self._first_wins_probability(p1, p2) + (1 - self._first_wins_probability(p2, p1))) / 2
        if prob_1 >= 0.5:
            winner, confidence = p1["Name"].title(), prob_1
        else:
            winner, confidence = p2["Name"].title(), 1 - prob_1
        return {"vencedor": winner, "confianca": round(float(confidence), 4)}
