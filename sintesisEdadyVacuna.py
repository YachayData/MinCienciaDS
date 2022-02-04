import pandas as pd
import numpy as np
import requests
import seaborn as sns
from matplotlib import pyplot as plt

# Recuperar los datos del Min Ciencia
url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto89/incidencia_en_vacunados_edad.csv"
res = requests.get(url, allow_redirects=True)

with open("dosis.csv", "wb") as file:
    file.write(res.content)

df = pd.read_csv("dosis.csv")

df["casos_confirmados"] = df["casos_confirmados"].astype(int)
#df["casos_uci"] = df["casos_uci"].astype(int)
#df["casos_def"] = df["casos_def"].astype(int)
#df["poblacion"] = df["poblacion"].astype(int)



ult_sem = df.semana_epidemiologica.unique()[-12:]


df12 = df[df.semana_epidemiologica.isin(ult_sem)] # filtrar 12 ultimas semanas

df12 = df12[df12.grupo_edad != '06 - 11 años']

df12["p_casos_confirmados"] = df12.poblacion / df12.casos_confirmados
df12["p_casos_uci"] = df12.poblacion / df12.casos_uci

df12["p_casos_def"] = df12.poblacion / df12.casos_def

df12["p_casos_confirmados"] = df12["p_casos_confirmados"]
df12["p_casos_uci"] = df12["p_casos_uci"]
df12["p_casos_def"] = df12["p_casos_def"]

df12["p_casos_uci_str"] = df12["p_casos_uci"].astype('str')

#df12.estado_vacunacion = df12.estado_vacunacion.astype('category')

pivot_confirmados = df12.pivot_table(values = "p_casos_confirmados", columns = "estado_vacunacion", index = "grupo_edad").astype(int)
pivot_uci = df12.pivot_table(values = "p_casos_uci", columns = "estado_vacunacion", index = "grupo_edad")
pivot_def = df12.pivot_table(values = "p_casos_def", columns = "estado_vacunacion", index = "grupo_edad")

cols = ['sin esquema completo',
 'con esquema completo',
 'con dosis refuerzo > 14 dias']

pivot_confirmados = pivot_confirmados[cols]
pivot_uci = pivot_uci[cols]
pivot_def = pivot_def[cols]


import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(1,3)

sns.set(font="Arial")
g = sns.heatmap(data = pivot_confirmados , cmap = 'RdYlGn', annot = True, square = True, ax = ax1, fmt= 'd')#, cbar = None)
g = sns.heatmap(data = pivot_uci , cmap = 'RdYlGn', annot = True, square = True, ax = ax2)#, cbar = None)
g = sns.heatmap(data = pivot_def , cmap = 'RdYlGn', annot = True, square = True, ax = ax3)#, cbar = None)
plt.show(block=False)


plt.savefig('sintesisEdad.pdf')