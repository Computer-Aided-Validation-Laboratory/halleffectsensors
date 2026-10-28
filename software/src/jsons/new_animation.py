from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from scipy.interpolate import griddata

# Load data
data_path = Path(__file__).parent / "animation_data.csv"
data = pd.read_csv(data_path)

rows = data.shape[0]
timestamps = data.iloc[:, 0].to_numpy()


x_coordinates = [0, 1, 0, 1]
y_coordinates = [0, 0, 1, 1]

xi = np.linspace(0, 1, 100)
yi = np.linspace(0, 1, 100)
x, y = np.meshgrid(xi, yi)

vmin = data.iloc[:, 1:].min().min()
vmax = data.iloc[:, 1:].max().max()

data_plot = data.iloc[0].to_numpy()[1:]

z = griddata((x_coordinates, y_coordinates),data_plot,(x, y),method="cubic")
fig, ax = plt.subplots()
img = ax.imshow(z,origin="lower",extent=(0, 1, 0, 1),cmap="viridis",
                vmin=vmin,vmax=vmax,animated=True)
scatter = ax.scatter(x_coordinates,y_coordinates,c="red",s=50)

cbar = fig.colorbar(img)
cbar.set_label("count value")

title = ax.set_title(f"t = {timestamps[0]:.2f} s")
ax.set_xlabel("x")
ax.set_ylabel("y")

all_z =[]

for entry in range(rows):
    data_plot = data.iloc[entry].to_numpy()[1:]
    z = griddata((x_coordinates, y_coordinates),data_plot,(x, y),method="linear")
    all_z.append(z)

def update(frame):
    '''d'''
    img.set_data(all_z[frame])
    title.set_text(f"t = {timestamps[frame]:.2f} s")
    return img, title

ani = animation.FuncAnimation(fig,update,frames=rows,interval=100,blit=True)

writer = animation.FFMpegWriter(fps=10,bitrate=1800)
save_path = Path(__file__).parent /"field_animation.mp4"
ani.save(save_path,writer=writer)

plt.show()


# job for this afternoon is to put this into other code so can use bigger arrays
