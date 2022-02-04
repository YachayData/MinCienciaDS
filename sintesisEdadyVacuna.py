import pandas as pd
import numpy as np
import requests

# Recuperar los datos del Min Ciencia
url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto89/incidencia_en_vacunados_edad.csv"
res = requests.get(url, allow_redirects=True)

with open("dosis.csv", "wb") as file:
    file.write(res.content)

df = pd.read_csv("dosis.csv")

ult_sem = df.semana_epidemiologica.unique()[-12:]

df12 = df[df.semana_epidemiologica.isin(ult_sem)] # filtrar 12 ultimas semanas
df12["p_casos_confirmados"] = df12.poblacion / df12.casos_confirmados
df12 = df12.groupby(["grupo_edad", "estado_vacunacion"]).mean()["p_casos_confirmados"]
print(df12)