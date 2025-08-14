import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from imports import *
from modelo_treinado.model import train
from predicoes.prediction import prever_ganhador

print(prever_ganhador("Growlithe","Vulpix"))