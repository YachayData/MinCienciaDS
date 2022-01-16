import pandas as pd 
import numpy as np
import requests

# Recuperar los datos del Min Ciencia

url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto90/incidencia_en_vacunados.csv'
res = requests.get(url, allow_redirects=True)
with open('dosis.csv','wb') as file:
    file.write(res.content)

df = pd.read_csv('dosis.csv')
my_df = df[['sin_vac_uci','una_dosis_uci', 'dos_dosis_uci', 'dos_dosis_comp_uci']]

# Población objetivo
obj = 3044845 + 15200840

# Datos de la última semana
dfl = df.iloc[-1,:]

# Obtener las personas con 3 dosis y con 2 dosis
dose3 = dfl.iloc[-1]
dose2 = dfl.iloc[-2]

# Calcular esto en base 900.
# Da el número de circulitos de cada categoría

dose3_p = dose3 / obj * 900
dose2_p = dose2 / obj * 900

print('Si Chile fuera 900 personas:')
print(dose3_p, 'personas con 3 dosis')
print(dose2_p, 'personas con 2 dosis')
print(900 - dose3_p - dose2_p, 'personas sin dosis')
print('---')

# Para obtener una estimación de los casos UCI
# se utilizan los datos de las 5 últimas semanas

res = my_df.iloc[-5:,:].sum()

print(res) 

# gives 
# sin dosis tenemos 6
# con dos dosis: 0.06
# cos tres dosis tenemos 3