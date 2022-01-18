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

dose3_uci_p = dose3_uci / sum_uci * 9
dose2_uci_p = dose2_uci / sum_uci * 9
dose0_uci_p = dose0_uci / sum_uci * 9

print("Para 9 personas en UCI:")
print(dose3_uci_p, "personas con resfuerzo")
print(dose2_uci_p, "con pauta completa")
print(dose0_uci_p, "sin pauta completa")
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


x_uci = np.arange(3) + 5
y_uci = np.arange(3) + 35
xv, yv = np.meshgrid(x_uci, y_uci)

plt.scatter(xv, yv, s=80, color=my_pink)

val3 = np.round(dose3_uci_p)
val2 = np.round(dose2_uci_p)

index = 0
xvr = xv.ravel()
yvr = yv.ravel()

while index < val3:
    #plt.scatter(xvr[index], yvr[index], s=80, color=my_green)
    plt.scatter(xvr[index], yvr[index], s=80, color=my_green)
    index += 1

index2 = 0
while index2 < val2:
    plt.scatter(xvr[index], yvr[index], s=80, color=my_blue)
    index2 += 1
    index += 1

plt.text(3.75, 33.5, "Ingresos UCI")
plt.text(2, 32.5,"(promedio 5 semanas)")

plt.legend(loc="upper right", bbox_to_anchor=(.97, .97))

#ax.set(xticklabels=[])  # remove the tick labels
#ax.tick_params(left=False)  # remove the ticks

#val = 0.25
#plt.text(-0.75, 1-val, '1')
#plt.text(-0.75, 10-val, '10')
#plt.text(-0.75, 20-val, '20')
#plt.text(-0.75, 30-val, '30')
plt.axis("off")
plt.show(block=False)
