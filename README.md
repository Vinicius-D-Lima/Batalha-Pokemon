# Batalha Pokémon

Prevê o vencedor de uma batalha entre dois Pokémon usando Machine Learning. O projeto tem:

- **API** (FastAPI) com um modelo `GradientBoostingClassifier` treinado em ~50 mil combates;
- **App mobile/web** (Expo + React Native) para escolher dois Pokémon e ver o resultado.

O modelo usa os seis stats base de cada Pokémon e a vantagem de tipos entre eles
(`backend/ml/type_chart.py`). Acurácia no conjunto de teste: ~92,7%.

## Estrutura

```
backend/
  app/        API FastAPI (main.py, schemas.py)
  ml/         dados, features, treino e previsão
  data/       pokemon.csv e combats.csv
  tests/      testes (pytest)
mobile/       app Expo / React Native
.github/      CI (pytest)
```

## Rodando a API

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

python -m ml.train                                   # treina e salva o modelo (opcional)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Se o modelo ainda não tiver sido treinado, a API treina automaticamente ao iniciar.
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
cd mobile
cp .env.example .env     # ajuste EXPO_PUBLIC_API_URL para o IP da sua máquina
npm install
npm start
```

## Testes

```bash
cd backend
python -m pytest
```
