import numpy as np
import pandas as pd
import seaborn as sns
import joblib   
import matplotlib.pyplot as plt 
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

for dirname, _, filenames in os.walk("./data"):
    for filename in filenames:
        print(os.path.join(dirname,filename))


print("rodou os imports")