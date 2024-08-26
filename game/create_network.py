import pandas as pd
import os

os.chdir('../assets/network/')


data = pd.read_csv('TestNetwork.csv')

print(data)