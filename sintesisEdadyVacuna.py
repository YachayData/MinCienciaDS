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
df12["p_casos_uci_str"] = df12["p_casos_uci"].astype('str')

#df12.estado_vacunacion = df12.estado_vacunacion.astype('category')

pivot_poblacion = df12.pivot_table(values = "poblacion", columns = "estado_vacunacion", index = "grupo_edad")
pivot_confirmados = df12.pivot_table(values = "p_casos_confirmados", columns = "estado_vacunacion", index = "grupo_edad")
pivot_uci = df12.pivot_table(values = "p_casos_uci", columns = "estado_vacunacion", index = "grupo_edad")
pivot_def = df12.pivot_table(values = "p_casos_def", columns = "estado_vacunacion", index = "grupo_edad")

cols = ['sin esquema completo',
 'con esquema completo',
 'con dosis refuerzo > 14 dias']


pivot_poblacion = pivot_poblacion.values
pivot_confirmados = pivot_confirmados[cols].values
pivot_uci = pivot_uci[cols].values
pivot_def = pivot_def[cols].values

vals_uci = np.zeros(pivot_uci.shape, dtype = int)
vals_def = np.zeros(pivot_def.shape, dtype = int)

mask_uci = np.zeros(pivot_uci.shape, dtype = bool)
mask_def = np.zeros(pivot_def.shape, dtype = bool)

pivot_uci_str = np.zeros(pivot_uci.shape, dtype=object)
pivot_def_str = np.zeros(pivot_def.shape, dtype=object)

for i in range(pivot_uci_str.shape[0]):
    for j in range(pivot_uci_str.shape[1]):

        if not np.isinf(pivot_uci[i, j]):
            mask_uci[i, j] = False
            vals_uci[i, j] = int(pivot_uci[i, j])
            pivot_uci_str[i, j] = str(vals_uci[i, j])            
        else:
            mask_uci[i, j] = True
            vals_uci[i, j] = int(pivot_poblacion[i, j])
            pivot_uci_str[i, j] = '>\n' + str(vals_uci[i, j])
            
        if not np.isinf(pivot_def[i, j]):
            mask_def[i, j] = False
            vals_def[i, j] = int(pivot_def[i, j])
            pivot_def_str[i, j] = str(vals_def[i, j])            
        else:
            mask_def[i, j] = True
            vals_def[i, j] = int(pivot_poblacion[i, j])
            pivot_def_str[i, j] = '>\n' + str(vals_uci[i, j])


import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize = (40,8))

sns.set(font="Arial")
g = sns.heatmap(data = pivot_confirmados , cmap = 'RdYlGn', annot = True, square = True, ax = ax1, fmt= '.0f', cbar = None)
g = sns.heatmap(data = vals_uci , cmap = 'RdYlGn', annot = pivot_uci_str, square = True, ax = ax2, cbar = None, fmt = '', mask = mask_uci)
g = sns.heatmap(data = np.ones(vals_uci.shape), cmap = 'Blues', annot = pivot_uci_str, square = True, ax = ax2, cbar = None, fmt = '', mask = ~mask_uci, color = 'g')

g = sns.heatmap(data = vals_def , cmap = 'RdYlGn', annot = pivot_def_str, square = True, ax = ax3, fmt= '', cbar = None, mask = mask_def)
g = sns.heatmap(data = np.ones(vals_def.shape), cmap='Blues', annot = pivot_def_str, square = True, ax = ax3, cbar = None, fmt = '', mask = ~mask_def, color = 'g')
plt.show(block=False)


plt.savefig('sintesisEdad.pdf')