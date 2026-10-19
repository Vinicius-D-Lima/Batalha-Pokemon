# Batalha Pokémon

Prevê o vencedor de uma batalha entre dois Pokémon usando Machine Learning. O projeto tem:

- **API** (FastAPI) com um modelo `GradientBoostingClassifier` treinado em ~50 mil combates;
- **App mobile/web** (Expo + React Native) para escolher dois Pokémon e ver o resultado.

O modelo usa os seis stats base de cada Pokémon e a vantagem de tipos entre eles
(`predicoes/type_chart.py`). Acurácia no conjunto de teste: ~92,7%.

## Estrutura

```
main.py              API FastAPI
modelo_treinado/     treino e carregamento do modelo
predicoes/           lógica de previsão e tabela de tipos
utils/               leitura e pré-processamento dos CSVs
data/                pokemon.csv e combats.csv
tests/               testes (pytest)
react-native/        app Expo
```

## Rodando a API

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m modelo_treinado.model                      # treina e salva o modelo (opcional)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Se o modelo ainda não tiver sido treinado, a API treina automaticamente na primeira requisição.
Documentação interativa em http://127.0.0.1:8000/docs.

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/prever \
  -H "Content-Type: application/json" \
  -d '{"nome1": "Charizard", "nome2": "Blastoise"}'
# {"vencedor": "Charizard", "confianca": 0.9472}
```

Nomes inexistentes retornam HTTP 404.

## Rodando o app

```bash
cd react-native
cp .env.example .env     # ajuste EXPO_PUBLIC_API_URL para o IP da sua máquina
npm install
npm start
```

## Testes

```bash
python -m pytest
```
