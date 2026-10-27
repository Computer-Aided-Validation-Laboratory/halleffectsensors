import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

json_path = Path(__file__).parent.parent/'jsons'/'example.json'
data_path = Path(__file__).parent.parent/'jsons'/'example_data.csv'

data_frame = pd.read_csv(data_path)

with open(json_path, encoding = 'utf-8') as f:
    sensors_data = json.load(f)


def split_data(data: pd.DataFrame, sensors: json):
    '''d'''
    rows = data.shape[0]

    num_x = 0
    num_y = 0
    num_z = 0

    for sensor in sensors["sensors"]:
        if sensor["direction"] == "x":
            num_x+=1
        elif sensor["direction"] == "y":
            num_y +=1
        elif sensor["direction"] == "z":
            num_z +=1
        else:
            print("direction error, check .json")

    x_dataframe = pd.DataFrame(np.zeros((rows, (num_x+1))), dtype = float)
    y_dataframe = pd.DataFrame(np.zeros((rows, (num_y+1))), dtype = float)
    z_dataframe = pd.DataFrame(np.zeros((rows, (num_z+1))), dtype = float)

    i = x = z = y = 0

    for sensor in sensors["sensors"]:
        i +=1
        if sensor["index"] == i:
            if sensor["direction"] == "x":
                x_dataframe[x_dataframe.columns[x+1]] = data[data.columns[i]]
                x+=1
            elif sensor["direction"] == "y":
                y_dataframe[y_dataframe.columns[y+1]] = data[data.columns[i]]
                y+=1
            elif sensor["direction"] == "z":
                z_dataframe[z_dataframe.columns[z+1]] = data[data.columns[i]]
                z+=1

    x_dataframe[x_dataframe.columns[0]] = data[data.columns[0]]
    y_dataframe[y_dataframe.columns[0]] = data[data.columns[0]]
    z_dataframe[z_dataframe.columns[0]] = data[data.columns[0]]

    return x_dataframe, y_dataframe, z_dataframe, num_x, num_y, num_z

def x_plot(data: pd.DataFrame, number:int, sensors):
    '''d'''
    x_coord = np.empty(number)
    y_coord = np.empty(number)
    index = 0

    for sensor in sensors["sensors"]:
        if sensor["direction"] == "x":
            x_coord[index] = sensor["coordinate"][0]
            y_coord[index] = sensor["coordinate"][1]
            index += 1

    timestamps = data[data.columns[0]].to_numpy()
    print(data[data.columns[0]])

    xi = np.linspace(0, 1, 100)
    yi = np.linspace(0, 4, 100)
    X, Y = np.meshgrid(xi, yi)

    fig, ax = plt.subplots()
    cbar = None

    for i in range(number):
        data[data.columns[i+1]] = (((data[data.columns[i+1]])*5/1023)-2.5)*1000/31.25

    for t in range(data.shape[0]):

        values = data.iloc[t, 1:11].to_numpy()

        Z = griddata((x_coord, y_coord),values,(X, Y),method='cubic')

        ax.clear()
        im = ax.contourf(X, Y, Z, levels=100, cmap='viridis')
        ax.scatter(x_coord, y_coord, c='red', s=50)
        ax.set_title(f"t={timestamps[t]:.2f} s")

        if cbar is not None:
            cbar.remove()
        cbar = fig.colorbar(im)

        plt.pause(0.25)

    plt.show()


if __name__ == "__main__":
    x_data, y_data, z_data, x_num, y_num, z_num = split_data(data = data_frame, sensors = sensors_data)
    x_plot(data = x_data, number = x_num, sensors = sensors_data)
