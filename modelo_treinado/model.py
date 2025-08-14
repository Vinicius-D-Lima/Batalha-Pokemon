import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from imports import *   
from utils.pre_process_data import pré_processamento
from predicoes.type_chart import type_chart

pokemon,batalha = pré_processamento()
def calc_total_vantagem(tipo_atacante,tipo_defensor):
    multiplier = 1.0
    for atk_type in tipo_atacante:
        if pd.notna(atk_type):
            for def_type in tipo_defensor:
                if pd.notna(def_type):
                    multiplier *= type_chart.get(atk_type.lower(),{}).get(def_type.lower(),1.0)
    return multiplier

def train():
    pokemon.rename(columns = {'#' :'id'},inplace = True)

    poke1 = pokemon.add_suffix('_1')
    poke1.rename(columns = {'id_1' : 'First_pokemon'},inplace = True)
    poke2 = pokemon.add_suffix('_2')
    poke2.rename(columns = {'id_2' : 'Second_pokemon'},inplace = True)

    df = batalha.merge(poke1, on = 'First_pokemon').merge(poke2, on = 'Second_pokemon')
    df['ganhador_label'] = (df['Winner'] == df['First_pokemon']).astype(int)
    df['type_advantage_1'] = df.apply(lambda row:  calc_total_vantagem([row['Type 1_1'],row['Type 2_1']],[row['Type 1_2'],row['Type 2_2']]),axis = 1)
    df['type_advantage_2'] = df.apply(lambda row:  calc_total_vantagem([row['Type 1_2'],row['Type 2_2']],[row['Type 1_1'],row['Type 2_1']]),axis = 1)

    features = [
        'HP_1', 'Attack_1', 'Defense_1', 'Sp. Atk_1', 'Sp. Def_1', 'Speed_1',
        'HP_2', 'Attack_2', 'Defense_2', 'Sp. Atk_2', 'Sp. Def_2', 'Speed_2',
        'type_advantage_1', 'type_advantage_2'
    ]

    X = df[features]
    y = df['ganhador_label']

    #aqui eu normalizei os status dividindo eles por 100 para entrar na escala de 1 ate 0
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()

    X_scaled = scaler.fit_transform(X)

    X_train,X_test, y_train,y_test = train_test_split(X_scaled,y,test_size=0.2, random_state = 42)
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    model.fit(X_train,y_train)

    joblib.dump(model,'modelo_pokemon.pkl')
    print("rodou o modelo")
    return model,features,X_test,y_test