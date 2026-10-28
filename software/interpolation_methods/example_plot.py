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

    Methods:
        get_data() -> None:
            loads in the .json and .csv file and assigns them to variables
        split_data() -> None:
            calculates how many of each directioned sensor is present and creates data
            frames for each direction and stores the correct data in it
        plot_map() -> None:
            plots the field map at every timestamp for the specified direction.
    '''

    def __init__(self, json_file: str, data: str, direction:str):
        
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

        self.img = None
        self.fig = None
        self.title = None
        self.rows = None
        self.all_z = None

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

        for i in range((self.data.shape[1]-1)):
            self.data[self.data.columns[i+1]] = ((self.data[self.data.columns[i+1]]-512)*5/1023)*1000/31.25

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
        '''
        determines which direction of field is wanting to be plotted, plots the animation
        and saves it as an mp4 file
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
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        self.all_z = []

        for entry in range(self.rows):
            self.plotting = self.data.iloc[entry].to_numpy()[1:]
            z = griddata((self.x_coords, self.y_coords), self.plotting, (x, y), method = 'cubic')
            self.all_z.append(z)

    def update(self, frame: int) -> None:
        '''
        update function for the animation.FuncAnimation in run()
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
            filename (str): name of the file that the animation is saved to
        Returns:
            None
        '''
        self.split_data()
        self.plot_map()

        ani = animation.FuncAnimation(self.fig, self.update, frames=self.rows, interval=100, blit =True )
        plt.show()
        writer = animation.FFMpegWriter(fps=10, bitrate=1800)
        save_path = Path(__file__).parent/filename
        ani.save(save_path, writer = writer)


if __name__ == "__main__":
    a = Plotting(json_file = 'calib.json',data = 'cal_9(6-12)(11.1).csv', direction = "z" )
    a.run(filename = 'animation.mp4')
