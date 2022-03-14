import WazeRouteCalculator
from WazeRouteCalculator import logging
import time 
import pandas as pd 

real_time_list = [True, False]

logger = logging.getLogger("WazeRouteCalculator.WazeRouteCalculator")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)
region = "EU"

cities = ['Tomeco', 'Copiulemu']
results = []

ta = time.ctime()



for real_time in real_time_list:


	from_address = cities[0] + ' Centro, Chile'
	to_address = cities[-1] + ' Centro, Chile'

	route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
	res = route.calc_route_info(real_time=real_time)
	results.append([ta, cities[0], cities[-1], res[0], res[1], real_time])

	from_address = cities[-1] + ' Centro, Chile'
	to_address = cities[0] + ' Centro, Chile'
	route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
	res = route.calc_route_info(real_time=real_time)

	results.append([ta, cities[-1], cities[0], res[0], res[1], real_time])

df = pd.DataFrame(results, columns = ['Fecha', 'From', 'To', 'Tiempo (min)', 'Distancia (km)', 'Real Time'])
df['Velocidad promedia'] = df['Distancia (km)'] /( df['Tiempo (min)'] / 60.)


df.to_csv('results/' + str(ta) + '.csv', index = False)

