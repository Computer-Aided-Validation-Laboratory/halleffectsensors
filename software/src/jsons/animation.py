# try make it displayed as an animation so it can be saved, then will put this into plot.py

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from scipy.interpolate import griddata

data_path = Path(__file__).parent/'animation_data.csv'
data = pd.read_csv(data_path)


rows = data.shape[0]
columns = data.shape[1]

timestamps = np.empty(rows)
timestamps = data[data.columns[0]].to_numpy()

data_plot = data.iloc[1].to_numpy()
data_plot = np.delete(data_plot, 0)


x_coordinates = [0,1,0,1]
y_coordinates = [0,0,1,1]

xi = np.linspace(0,1,100)
yi = np.linspace(0,1,100)
x,y = np.meshgrid(xi,yi)

fig, ax = plt.subplots()

z = griddata((x_coordinates, y_coordinates), data_plot, (x,y), method = 'cubic')
im = ax.contourf(x, y, z, levels = 100, cmap = 'viridis')
scatter = ax.scatter(x_coordinates, y_coordinates)
cbar = fig.colorbar(im)

plt.show()
