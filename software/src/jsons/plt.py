import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

class Plot:
    '''
    d
    '''

    def __init__(self, choice: str):

        self.choice = choice

        self.data = None
        self.x_data = None
        self.y_data = None
        self.z_data = None
        self.sensors = None
        self.timestamps = None
        self.num_x = 0
        self.num_y = 0
        self.num_z= 0

        self.get_data()

    def get_data(self) -> None:
        '''d'''
        json_path = Path(__file__).parent/'example.json'
        data_path = Path(__file__).parent/'example_data.csv'

        self.data = pd.read_csv(data_path)

        with open(json_path, encoding = 'utf-8') as f:
            self.sensors = json.load(f)

        self.split_data()

    def split_data(self) -> None:
        '''d'''
        rows = self.data.shape[0]

        for sensor in self.sensors["sensors"]:
            if sensor["direction"] == "x":
                self.num_x += 1
            elif sensor["direction"] == "y":
                self.num_y += 1
            else:
                self.num_z += 1

        self.x_data = pd.DataFrame(np.zeros((rows,(self.num_x+1))),dtype = float)
        self.y_data = pd.DataFrame(np.zeros((rows,(self.num_y+1))),dtype = float)
        self.z_data = pd.DataFrame(np.zeros((rows,(self.num_z+1))),dtype = float)

        self.x_data[self.x_data.columns[0]] = self.data[self.data.columns[0]]
        self.y_data[self.y_data.columns[0]] = self.data[self.data.columns[0]]
        self.z_data[self.z_data.columns[0]] = self.data[self.data.columns[0]]

        i = x = y = z = 0

        for sensor in self.sensors["sensors"]:
            i+=1
            if sensor["index"] == i:
                if sensor["direction"] == "x":
                    self.x_data[self.x_data.columns[x+1]] = self.data[self.data.columns[i]]
                    x+=1
                elif sensor["direction"] == "y":
                    self.y_data[self.y_data.columns[y+1]] = self.data[self.data.columns[i]]
                    y+=1
                elif sensor["direction"] == "z":
                    self.z_data[self.z_data.columns[z+1]] = self.data[self.data.columns[i]]
                    z+=1

        self.plot()

    def plot(self) -> None:
        '''d'''


        if self.choice == "x":
            number = self.num_x
            data = self.x_data
        elif self.choice == "y":
            number = self.num_y
            data = self.y_data
        else:
            number = self.num_z
            data = self.z_data

        x_coord = np.empty(number)
        y_coord = np.empty(number)
        index = 0

        for sensor in self.sensors["sensors"]:
            if sensor["direction"] == "x":
                x_coord[index] = sensor["coordinate"][0]
                y_coord[index] = sensor["coordinate"][1]
                index+=1

        self.timestamps = self.data[self.data.columns[0]].to_numpy()

        xi = np.linspace(0,1,100)
        yi = np.linspace(0,4,100)
        X,Y = np.meshgrid(xi,yi)

        fig, ax = plt.subplots()
        cbar = None

        for i in range(number):
            data[data.columns[i+1]] = ((data[data.columns[i+1]]*5/1023)-2.5)*1000/31.25

        for t in range(data.shape[0]):
            values = data.iloc[t, 1:11].to_numpy()

            Z = griddata((x_coord,y_coord), values, (X,Y), method ='cubic')
            ax.clear()
            im = ax.contourf(X, Y, Z, levels=100, cmap='viridis')
            ax.scatter(x_coord, y_coord, c = 'red', s = 50)
            ax.set_title(f"t={self.timestamps[t]:.2f} s")

            if cbar is not None:
                cbar.remove()
    
            cbar = fig.colorbar(im)

            plt.pause(0.25)

        plt.show()

if __name__ == "__main__":
    a = Plot(choice="x")
