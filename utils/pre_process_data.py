from imports import *
from utils.data_loader import data_loading

def pré_processamento():

    df_pokemon, df_batalha = data_loading('data\pokemon(1).csv','data\combats.csv')

    missing_values = df_pokemon.isnull().sum()
    print('Missing values in each column:')
    print(missing_values)
    df_pokemon['Type 2'] = df_pokemon['Type 2'].fillna('None')
    df_pokemon['Name'] = df_pokemon['Name'].str.lower()


    return df_pokemon, df_batalha