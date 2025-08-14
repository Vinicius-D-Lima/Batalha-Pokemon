import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from imports import *
from modelo_treinado.model import train
from utils.pre_process_data import pré_processamento
from modelo_treinado.model import calc_total_vantagem



model,features,X_test,y_test = train()
pokemon,batalha = pré_processamento()


def prever_ganhador(nome1,nome2):

    p1 = pokemon[pokemon['Name'].str.lower() == nome1.lower()]
    p2 = pokemon[pokemon['Name'].str.lower() == nome2.lower()]



    if p1.empty or p2.empty:
        return "Um dos nomes está incorreto. Verifique a grafia."
    

    stats1 = p1[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].iloc[0]
    stats2 = p2[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].iloc[0]

    type_adv1 = calc_total_vantagem([p1['Type 1'].values[0], p1['Type 2'].values[0]], 
                                [p2['Type 1'].values[0], p2['Type 2'].values[0]])
    type_adv2 = calc_total_vantagem([p2['Type 1'].values[0], p2['Type 2'].values[0]], 
                                [p1['Type 1'].values[0], p1['Type 2'].values[0]])

    print("Vantagem de tipos:", type_adv1, type_adv2)




    input_data = pd.DataFrame([list(stats1) + list(stats2) + [type_adv1, type_adv2]],columns= features)

    resultado = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0]
    log_prob = model.predict_log_proba(input_data)[0]

    

    if resultado == 1:
        vencedor = nome1
        confiança_modelo = prob[1]
    else:
        vencedor = nome2
        confiança_modelo = prob[0]

    print("rodou a predicao")
    
    return (
    f"🏆 Provável vencedor: {vencedor}\n"
    f"🔢 Confiança ajustada: {confiança_modelo * 100:.2f}%\n")
