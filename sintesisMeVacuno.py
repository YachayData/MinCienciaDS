import pandas as pd
import numpy as np
import requests

# Recuperar los datos del Min Ciencia

url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto90/incidencia_en_vacunados.csv"
res = requests.get(url, allow_redirects=True)
with open("dosis.csv", "wb") as file:
    file.write(res.content)

df = pd.read_csv("dosis.csv")
my_df = df[
    [
        "sin_vac_uci",
        "una_dosis_uci",
        "dos_dosis_uci",
        "dos_dosis_comp_uci",
        "dosis_unica_uci",
        "dosis_unica_comp_uci",
        "dosis_ref_comp_uci",
    ]
]

my_df_fall = df[
    [
      'sin_vac_fall', 'una_dosis_fall', 'dos_dosis_fall',
       'dos_dosis_comp_fall', 'dosis_unica_fall', 'dosis_unica_comp_fall',
       'dosis_ref_comp_fall'
    ]
]

# Población objetivo
obj = 3044845 + 15200840

# Datos de la última semana
dfl = df.iloc[-1, :]

# Obtener las personas con esquema completo y con dosis de resfuerzo
# Esquema completo:
dose3 = dfl.personas_con_refuerzo
dose2 = dfl.personas_con_pauta_completa
dose0 = obj - dose2


# Calcular esto en base 900.
# Da el número de circulitos de cada categoría

dose3_p = dose3 / obj * 900
dose2_p = dose2 / obj * 900
dose0_p = dose0 / obj * 900

print("Si Chile fuera 900 personas:")
print(dose3_p, "personas con resfuerzo")
print(dose2_p, "con pauta completa")
print(dose0_p, "sin pauta completa")
print("---")

# Para obtener una estimación de los casos UCI
# se utilizan los datos de las 5 últimas semanas

res = my_df.iloc[-5:, :].sum()

sum_uci = res.sum()
print(sum_uci, "suma de los ingresos UCI últimas 5 semanas")

print(res)
print("----")

dose2_uci = res.dosis_unica_comp_uci + res.dos_dosis_comp_uci
dose3_uci = res.dosis_ref_comp_uci
dose0_uci = sum_uci - dose3_uci - dose2_uci

dose3_uci_p = dose3_uci / sum_uci * 30
dose2_uci_p = dose2_uci / sum_uci * 30
dose0_uci_p = dose0_uci / sum_uci * 30

print("Para 30 personas en UCI:")
print(dose3_uci_p, "personas con resfuerzo")
print(dose2_uci_p, "con pauta completa")
print(dose0_uci_p, "sin pauta completa")
print("---")


# Fallecidos en las 5 últimas semanas

res_fall = my_df_fall.iloc[-5:, :].sum()

sum_fall = res.sum()
print(sum_fall, "suma de los cassos fallecidos últimas 5 semanas")

print(res)
print("----")

dose2_fall = res_fall.dosis_unica_comp_fall + res_fall.dos_dosis_comp_fall
dose3_fall = res_fall.dosis_ref_comp_fall
dose0_fall = sum_fall - dose3_fall - dose2_fall

dose3_fall_p = dose3_fall / sum_fall * 30
dose2_fall_p = dose2_fall / sum_fall * 30
dose0_fall_p = dose0_fall / sum_fall * 30

print("Para 30 personas fallecidas:")
print(dose3_fall_p, "personas con resfuerzo")
print(dose2_fall_p, "con pauta completa")
print(dose0_fall_p, "sin pauta completa")
print("---")

# Generar el plot:

import matplotlib.pyplot as plt

my_pink = np.array([248, 0, 123]) / 256.0
my_green = np.array([0, 179, 98]) / 256.0
my_blue = np.array([0, 153, 230]) / 256.0

x = np.arange(30) + 1
xv, yv = np.meshgrid(x, x)


fig, ax = plt.subplots(figsize=(8, 8))


plt.scatter(xv, yv, s=80, color=my_pink, label="sin pauta completa")


val3 = np.round(dose3_p)
val2 = np.round(dose2_p) - np.round(dose3_p)

index = 0
xvr = xv.ravel()
yvr = yv.ravel()

while index < val3:
    if index == 0:
        plt.scatter(xvr[index], yvr[index], s=80, color=my_green, label="con resfuerzo")
    else:
        plt.scatter(xvr[index], yvr[index], s=80, color=my_green)
    index += 1

    if index == val3:
        print(yvr[index], 'altura verde')

index2 = 0
while index2 < val2:
    if index2 == 0:
        plt.scatter(
            xvr[index], yvr[index], s=80, color=my_blue, label="con pauta completa"
        )
    else:
        plt.scatter(xvr[index], yvr[index], s=80, color=my_blue)
    index2 += 1
    index += 1

    if index2 == val2:
        print(yvr[index], 'altura azul')


y_uci = np.arange(30) + 1
plt.scatter( -2 * np.ones(y_uci.shape[0]), y_uci, s=80, color=my_pink)

val3_uci = np.round(dose3_uci_p)
val2_uci = np.round(dose2_uci_p)

range3_uci = np.arange(val3_uci) + 1
range2_uci = np.arange(val2_uci) + 1 + val3_uci

plt.scatter( -2 * np.ones(range3_uci.shape[0]), range3_uci, s=80, color=my_green)
plt.scatter( -2 * np.ones(range2_uci.shape[0]), range2_uci, s=80, color=my_blue)


y_fall = np.arange(30) + 1
plt.scatter( 33 * np.ones(y_fall.shape[0]), y_fall, s=80, color=my_pink)

val3_fall = np.round(dose3_fall_p)
val2_fall = np.round(dose2_fall_p)

range3_fall = np.arange(val3_fall) + 1
range2_fall = np.arange(val2_fall) + 1 + val3_fall

plt.scatter( 33 * np.ones(range3_fall.shape[0]), range3_fall, s=80, color=my_green)
plt.scatter( 33 * np.ones(range2_fall.shape[0]), range2_fall, s=80, color=my_blue)


plt.legend(loc="upper center", bbox_to_anchor = (.5, 1.125))

plt.text( -2, 31, 'uci', ha='center', va='center')
plt.text( 33, 31, 'fallecidos', ha='center', va='center')
plt.axis("off")

plt.savefig('sintesis.pdf')

plt.show(block=False)
