import requests
import pandas as pd

url = "http://localhost:5000/api/tareas"
resp = requests.get(url)

print(resp.status_code)

datos = resp.json()

print(type(datos), len(datos))

df_ext = pd.DataFrame(datos)
print(df_ext.head())

print(df_ext.info())

print(df_ext.describe())