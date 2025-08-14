from imports import *
from predicoes.prediction import prever_ganhador
from fastapi import FastAPI
from pydantic import BaseModel
from predicoes.type_chart import type_chart

app = FastAPI()

class pokemonRequest(BaseModel):
    nome1: str
    nome2: str

@app.get("/")
def home():
    return {"mensagem": "API de IA Pokémon online!"}

@app.post("/prever")
def prever_batalha(data:pokemonRequest):
    resultado = prever_ganhador(data.nome1,data.nome2)
    return {"resultado": resultado}


# para rodar a api localmente 
# digitar no terminal :
# python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
# se tudo estiver certo acesse no navegador:
# http://127.0.0.1:8000
# E para testar a API via formulário interativo (Swagger):
# http://127.0.0.1:8000/docs

#192.168.1.71








#def main():
 #   name1 = input("digite o nome do primeiro pokemon: ")
  #  name2 = input("digite o nome do seguundo pokemon: ")

   # result = prever_ganhador(name1,name2)
  #  print(result)

#if __name__ == '__main__':
   # main()