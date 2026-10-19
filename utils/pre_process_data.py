from utils.data_loader import data_loading


def pré_processamento():
    """Carrega e limpa os dados: Type 2 vazio vira 'None' e nomes ficam em minúsculas."""
    df_pokemon, df_batalha = data_loading()

    df_pokemon["Type 2"] = df_pokemon["Type 2"].fillna("None")
    df_pokemon["Name"] = df_pokemon["Name"].str.lower()
    df_pokemon = df_pokemon.rename(columns={"#": "id"})

    return df_pokemon, df_batalha
