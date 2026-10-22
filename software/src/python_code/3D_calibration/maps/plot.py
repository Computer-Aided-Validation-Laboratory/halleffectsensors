'''going to attempt to plot each field results? no clue what this will look like but we will see'''

# first need to get our three dataframes containing the field measurements

import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

FIELD = 17.4 # (field in cal_10(6-12)(17.4-3))

data_path = Path(__file__).parent / 'csv'

data_path = Path(__file__).parent / 'map_data.csv'
data = pd.read_csv(data_path)

path_json = Path(__file__).parent
json_output = path_json / 'plot.json'

with open(json_output, encoding = 'utf-8') as f:
    sensors = json.load(f)

x_coord = np.empty(9)
y_coord = np.empty(9)

for sensor in sensors["sensors"]:
    index = sensor["index"]-1
    x_coord[index] = sensor["position"][0]
    y_coord[index] = sensor["position"][1]

difference = np.empty(9)

for i in range(9):
    data[data.columns[i+1]] = data[data.columns[i+1]]*5/1023
    data[data.columns[i+1]] = data[data.columns[i+1]]-2.5
    data[data.columns[i+1]] = (data[data.columns[i+1]]*1000)/31.25
    average = data[data.columns[i+1]].mean()
    #difference[i] = np.abs(FIELD - average)
    difference[i] = np.abs(average)

xi = np.linspace(0, 2, 100)
yi = np.linspace(0, 2, 100)
X, Y = np.meshgrid(xi, yi)

print(x_coord, y_coord)

Z = griddata((x_coord, y_coord), difference, (X, Y), method='cubic')

plt.figure(figsize=(6,5))
plt.contourf(X, Y, Z, levels=100, cmap='viridis')
plt.colorbar(label='field(mT)')
#plt.colorbar(label='change in field from measured (mT)')

plt.scatter(x_coord, y_coord, c='black', s=10)
plt.savefig('cal_9-sensor')
plt.show()

# this works well now, next steps (task for the morning is to make it so that it does one for every time? or like can give like one averaged one every 10 seconds and a new image flashes up?)
# also should do like bigger ones when got my new ADC and can use the helmholtz coil to make maps for each calibration stage or like iteration. can add some of this to repo
# should also start making my calibration README.md
# should put quick explaination of it in the actual README.md andthen put a link to the longer explaination for both 1D and 3D


# just to see if the push will work
