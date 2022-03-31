from matplotlib import pyplot as plt
import pandas as pd 
import seaborn as sns 

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('results') if isfile(join('results', f))]


all_df = []
for file in onlyfiles:
    df = pd.read_csv('results/' + file)# usecols=read_columns)
    all_df.append(df)

df = pd.concat(all_df)
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Real Time'] = df['Real Time'].astype(bool)
df[[ 'Tiempo (min)', 'Distancia (km)',
       'Velocidad promedia']] = df[[ 'Tiempo (min)', 'Distancia (km)',
       'Velocidad promedia']].astype(float)

df['From'] = df['From'].astype("category")
df['To'] = df['To'].astype("category")
test = df[(df.From == 'Tomeco') & (df['Real Time'] == True)]

#df = pd.read_csv('results/Sun Mar 27 20:33:17 2022.csv')

#sns.histplot(data = df, x = 'From', y = 'Tiempo (min)')
#plt.show(block=False)