'''script for visualising magnetic fields based on input data'''

import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from scipy.interpolate import griddata


class Plotting:
    '''
    class for producing a dynamic plot of the field strengths measured from a sensor array.
    Produces a plot in a specified direction using information from a specified .json file
    and data from a specified csv file. Plots the raw data (does the magnetic field
    conversion for you) so the input file needs to be in count form for all directions of
    sensors and not in field form for 1 direction.

    Attributes:
        drection (str): either "x", "y", or "z" depending on which field you want visualised
        json_file (str): the file containing correct information about this sensor array
        data (str): the data that is going to be plotted
        bits (int): bit depth of ADC used to ensure correct conversion of data

    Methods:
        get_data() -> None:
            loads in the .json and .csv file and assigns them to variables
        split_data() -> None:
            calculates how many of each directioned sensor is present and creates data
            frames for each direction and stores the correct data in it
        get_nulls_and_sens() -> None:
            gets the correct nulls and sensitivity values for the direction of data we are
            plotting and saves them
        convert() -> None:
            converts the input data to magnetic field measurements based on the correct
            nulls and sensitivities
        plot_map() -> None:
            plots the field map at every timestamp for the specified direction.
    '''

    def __init__(self, json_file:str, data:str, direction:str, bits:int):
        
        self.direction = direction
        self.bits = (2**bits)

        self.num_x = 0
        self.num_y = 0
        self.num_z = 0

        data_path = Path(__file__).parent.parent/'src'/'python_code'/'3D_array'/'calib_data'/data
        self.data = pd.read_csv(data_path)

        json_path = Path(__file__).parent.parent/'src'/'python_code'/'3D_array'/json_file
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

        self.img = None
        self.fig = None
        self.title = None
        self.rows = None
        self.all_z = None

        self.sens = None
        self.nulls = None

    def split_data(self) -> None:
        '''
        calculates how many of each directioned sensor is present and creates data
        frames for each direction and stores the correct data in it
        Args:
            None
        Returns:
            None
        '''
        self.rows = self.data.shape[0]

        self.timestamps = self.data.iloc[:,0].to_numpy()

        for sensor in self.json["sensors"]:
            if sensor["direction"] == "x":
                self.num_x +=1
            elif sensor["direction"] == "y":
                self.num_y += 1
            elif sensor["direction"] == "z":
                self.num_z += 1

        self.x_data = pd.DataFrame(np.zeros((self.rows,(self.num_x+1))),dtype = float)
        self.y_data = pd.DataFrame(np.zeros((self.rows,(self.num_y+1))),dtype = float)
        self.z_data = pd.DataFrame(np.zeros((self.rows,(self.num_z+1))),dtype = float)

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

    def get_nulls_and_sens(self) -> None:
        '''
        choses which sensitivity values and which null voltages to use (x, y or z) based on the
        input direction and saves them to be used in the convert method
        Args:
            None
        Returns:
            None
        '''

        if self.direction == "x":
            self.data = self.x_data
            self.number = self.num_x
        elif self.direction == "y":
            self.data = self.y_data
            self.number = self.num_y
        elif self.direction == "z":
            self.data = self.z_data
            self.number = self.num_z

        self.sens = np.empty(self.number)
        self.nulls = np.empty(self.number)

        if self.direction == "x":
            sens_path = Path(__file__).parent.parent/'src'/'python_code'/'3D_array'/'csv'/'x_sens.csv'
        elif self.direction == "y":
            sens_path = Path(__file__).parent.parent/'src'/'python_code'/'3D_array'/'csv'/'y_sens.csv'
        else:
            sens_path = Path(__file__).parent.parent/'src'/'python_code'/'3D_array'/'csv'/'z_sens.csv'

        sens_df = pd.read_csv(sens_path, header = None)

        for i in range(self.number):
            self.sens[i] = (np.mean(sens_df[sens_df.columns[i]]))

        if self.json == '3D_calib_setup.json':
            nulls_file = 'nulls_and_uncertainties.csv'
        else:
            nulls_file = 'nulls_and_uns_1.csv'
        nulls_paths = Path(__file__).parent.parent/'src'/'python_code'/'3D_array'/'csv'/nulls_file
        nulls_df = pd.read_csv(nulls_paths, header = None)

        directions = nulls_df.shape[0] / 2

        if directions == 1:
            self.nulls = nulls_df.iloc[0]
        elif directions == 2:
            if self.num_x == 0:
                if self.direction == "y":
                    self.nulls = nulls_df.iloc[0]
                else:
                    self.nulls = nulls_df.iloc[1]
            elif self.num_y == 0:
                if self.direction == "x":
                    self.nulls = nulls_df.iloc[0]
                else:
                    self.nulls = nulls_df.iloc[1]
            elif self.num_z == 0:
                if self.direction == "y":
                    self.nulls = nulls_df.iloc[0]
                else:
                    self.nulls = nulls_df.iloc[1]
        elif directions == 3:
            if self.direction == "x":
                self.nulls = nulls_df.iloc[0]
            elif self.direction == "y":
                self.nulls = nulls_df.iloc[1]
            else:
                self.nulls = nulls_df.iloc[2]
            
    def convert(self) -> None:
        '''
        converts the data using sensitivity and null voltages measured from the calibration
        to be plotted as a magnetic field
        Args:
            None
        Returns:
            None
        '''

        for i in range(self.number):
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]]*6.144/self.bits
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]]-self.nulls[i]
            self.data[self.data.columns[i+1]] = abs(self.data[self.data.columns[i+1]]*1000/self.sens[i])

    def plot_map(self) -> None:
        '''
        plots the animation and saves it as an mp4 file
        Args:
            None
        Returns:
            None
        '''

        self.x_coords = np.empty(self.number)
        self.y_coords = np.empty(self.number)
        index = 0

        for sensor in self.json["sensors"]:
            if sensor["direction"] == self.direction:
                self.x_coords[index] = sensor["coordinate"][0]
                self.y_coords[index] = sensor["coordinate"][1]
                index += 1

        vmin = self.data.iloc[:, 1:].min().min()
        vmax = self.data.iloc[:, 1:].max().max()

        x_max = self.x_coords[0]
        x_min = self.x_coords[0]
    
        for i, coords in enumerate(self.x_coords):
            if self.x_coords[i] > x_max:
                x_max = coords
                x_max = self.x_coords[i]
            elif self.x_coords[i] < x_min:
                x_min = self.x_coords[i]

        y_max = self.y_coords[0]
        y_min = self.y_coords[0]

        for i, coords in enumerate(self.y_coords):
            if self.y_coords[i] > y_max:
                y_max = coords
                y_max = self.y_coords[i]
            elif self.y_coords[i] < y_min:
                y_min = self.y_coords[i]

        xi = np.linspace(x_min, x_max, 100)
        yi = np.linspace(y_min, y_max, 100)
        x, y = np.meshgrid(xi, yi)

        self.plotting = self.data.iloc[0].to_numpy()[1:]

        z = griddata((self.x_coords, self.y_coords), self.plotting, (x, y), method='cubic')
        self.fig, ax = plt.subplots()
        self.img = ax.imshow(z, origin = "lower", extent = (x_min, x_max, y_min, y_max), cmap = 'viridis',
                        vmin = vmin, vmax = vmax, animated = True)
        ax.scatter(self.x_coords, self.y_coords, c='black', s=30)

        cbar = self.fig.colorbar(self.img)
        cbar.set_label("field strengths (mT)")

        self.title = ax.set_title(f"t = {self.timestamps[0]:.2f} s")
        print(self.title)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        self.all_z = []

        for entry in range(self.rows):
            self.plotting = self.data.iloc[entry].to_numpy()[1:]
            z = griddata((self.x_coords, self.y_coords), self.plotting, (x, y), method = 'cubic')
            self.all_z.append(z)

    def update(self, frame: int) -> None:
        '''
        update function for the animation.FuncAnimation in run() method
        Args:
            frame (int): determines the length of the animation
        Returns:
            None
        '''

        self.img.set_data(self.all_z[frame])
        self.title.set_text(f"t = {self.timestamps[frame]/1000:.2f} s")
        return self.img, self.title

    def run(self, filename: str) -> None:
        '''
        runs all the methods in the class, runs the animation and saves the
        animation in specified filename
        Args:
            filename (str): name of the file that the animation is saved under
        Returns:
            None
        '''
        self.split_data()
        self.get_nulls_and_sens()
        self.convert()
        self.plot_map()

        ani = animation.FuncAnimation(self.fig, self.update, frames=self.rows, interval=100, blit =True)
        plt.show()
        writer = animation.FFMpegWriter(fps=20, bitrate=1800)
        save_path = Path(__file__).parent/filename
        ani.save(save_path, writer = writer)


if __name__ == "__main__":
    a = Plotting(json_file = '1D_calib_setup.json', data = 'cal_4.csv', direction = "z", bits = 15)
    a.run(filename = 'animation.mp4')
