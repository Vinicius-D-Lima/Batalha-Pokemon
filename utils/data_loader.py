import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from imports import *

def data_loading(pokemon,batalha):
    poke = pokemon
    battle = batalha
    df_pokemon = pd.read_csv(poke)
    df_batalha = pd.read_csv(battle)
    return df_pokemon,df_batalha