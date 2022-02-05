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
cols = ['sin esquema completo',
 'con esquema completo',
 'con dosis refuerzo > 14 dias']

index = ['80 años o más', '71 - 80 años', '61 - 70 años',
       '51 - 60 años', '41 - 50 años', '31 - 40 años', '21 - 30 años',
       '12 - 20 años', 'Total']

pivot_poblacion = df12.pivot_table(values = "poblacion", columns = "estado_vacunacion", index = "grupo_edad")[cols]
pivot_confirmados = df12.pivot_table(values = "p_casos_confirmados", columns = "estado_vacunacion", index = "grupo_edad")[cols]
pivot_uci = df12.pivot_table(values = "p_casos_uci", columns = "estado_vacunacion", index = "grupo_edad")[cols]
pivot_def = df12.pivot_table(values = "p_casos_def", columns = "estado_vacunacion", index = "grupo_edad")[cols]


pivot_poblacion_old = pivot_poblacion.values
pivot_confirmados_old = pivot_confirmados.values
pivot_uci_old = pivot_uci.values
pivot_def_old = pivot_def.values

vals_uci = np.zeros(pivot_uci.shape, dtype = int)
vals_def = np.zeros(pivot_def.shape, dtype = int)

mask_uci = np.zeros(pivot_uci.shape, dtype = bool)
mask_def = np.zeros(pivot_def.shape, dtype = bool)

pivot_uci_str = np.zeros(pivot_uci.shape, dtype=object)
pivot_def_str = np.zeros(pivot_def.shape, dtype=object)

for i in range(pivot_uci_str.shape[0]):
    for j in range(pivot_uci_str.shape[1]):

        if not np.isinf(pivot_uci_old[i, j]):
            mask_uci[i, j] = False
            vals_uci[i, j] = int(pivot_uci_old[i, j])
            pivot_uci_str[i, j] = str(vals_uci[i, j])            
        else:
            mask_uci[i, j] = True
            vals_uci[i, j] = int(pivot_poblacion_old[i, j])
            pivot_uci_str[i, j] = '>\n' + str(vals_uci[i, j])
            
        if not np.isinf(pivot_def_old[i, j]):
            mask_def[i, j] = False
            vals_def[i, j] = int(pivot_def_old[i, j])
            pivot_def_str[i, j] = str(vals_def[i, j])            
        else:
            mask_def[i, j] = True
            vals_def[i, j] = int(pivot_poblacion_old[i, j])
            pivot_def_str[i, j] = '>\n' + str(vals_uci[i, j])


import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize = (40,8))

sns.set(font="Arial")

vals_confirmados = pd.DataFrame(pivot_confirmados_old, columns = pivot_confirmados.columns, index = pivot_confirmados.index)
vals_uci = pd.DataFrame(vals_uci, columns = pivot_uci.columns, index = pivot_uci.index)
vals_def = pd.DataFrame(vals_def, columns = pivot_def.columns, index = pivot_def.index)

ax1.set_title('casos confirmados')
print('0')
g = sns.heatmap(data = vals_confirmados, cmap = 'RdYlGn', annot = True, square = True, ax = ax1, fmt= '.0f', cbar = None)
print('1')

ax2.set_title('casos uci')
#g = sns.heatmap(data = np.ones(vals_uci.shape), cmap = 'Blues', annot = pivot_uci_str, square = True, ax = ax2, cbar = None, fmt = '', mask = ~mask_uci, color = 'g')
g = sns.heatmap(data = vals_uci , cmap = 'RdYlGn', annot = pivot_uci_str, square = True, ax = ax2, cbar = None, fmt = '', mask = mask_uci)

print('2')
ax3.set_title('fallecimientos')
#g = sns.heatmap(data = np.ones(vals_def.shape), cmap='Blues', annot = pivot_def_str, square = True, ax = ax3, cbar = None, fmt = '', mask = ~mask_def, color = 'g')
g = sns.heatmap(data = vals_def , cmap = 'RdYlGn', annot = pivot_def_str, square = True, ax = ax3, fmt= '', cbar = None, mask = mask_def)

plt.show(block=False)


plt.savefig('sintesisEdad.pdf', bbox_inches='tight')