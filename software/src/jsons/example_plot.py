import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from scipy.interpolate import griddata


class Plotting:
    '''cds'''

    def __init__(self, json_file: str, data:str, direction:str):
        
        self.direction = direction

        self.num_x = 0
        self.num_y = 0
        self.num_z = 0

        data_path = Path(__file__).parent/data
        self.data = pd.read_csv(data_path)

        json_path = Path(__file__).parent/json_file
        with open(json_path, encoding = 'utf-8') as f:
            self.json = json.load(f)

        self.x_data = None
        self.y_data = None
        self.z_data = None

        self.timestamps = None
        self.number = None
        self.plotting = None

        self.x_coords = None
        self.y_coords = None

    def split_data(self) -> None:
        '''ds'''
        rows = self.data.shape[0]

        self.timestamps = self.data.iloc[:,0].to_numpy()

        for sensor in self.json["sensors"]:
            if sensor["direction"] == "x":
                self.num_x +=1
            elif sensor["direction"] == "y":
                self.num_y += 1
            elif sensor["direction"] == "z":
                self.num_z += 1

        self.x_data = pd.DataFrame(np.zeros((rows,(self.num_x+1))),dtype = float)
        self.y_data = pd.DataFrame(np.zeros((rows,(self.num_y+1))),dtype = float)
        self.z_data = pd.DataFrame(np.zeros((rows,(self.num_z+1))),dtype = float)

        self.x_data[self.x_data.columns[0]] = self.data[self.data.columns[0]]
        self.y_data[self.y_data.columns[0]] = self.data[self.data.columns[0]]
        self.z_data[self.z_data.columns[0]] = self.data[self.data.columns[0]]

        i = x = y = z = 0

        for sensor in self.json["sensors"]:
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


    def plot_map(self) -> None:
        '''ds'''

        if self.direction == "x":
            self.data = self.x_data
            self.number = self.num_x
        elif self.direction == "y":
            self.data = self.y_data
            self.number = self.num_y
        elif self.direction == "z":
            self.data = self.z_data
            self.number = self.num_z

        vmin = self.data.iloc[:, 1:].min().min()
        vmax = self.data.iloc[:, 1:].max().max()

        self.plotting = self.data.iloc[0].to_numpy()[1:]

        






        