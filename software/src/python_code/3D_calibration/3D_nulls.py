from pathlib import Path
from csv import writer
import numpy as np
import pandas as pd
from func import split_data


class Nulls:
    '''ds'''

    def __init__(self, number: int, port: str, vcc: float, filename: str,
                 vcc_un: float, resolution: int, samples: int = 400):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.filename = filename
        self.vcc_uncertainty = vcc_un
        self.bits = (2**resolution)-1
        self.samples = samples

        self.x = self.y = self.z = None
        self.nulls_x_df = self.nulls_y_df = self.nulls_z_df = None
        self.x_stds = self.y_stds = self.z_stds = None
        self.x_nulls = self.y_nulls = self.z_nulls = None
        self.x_nulls_un = self.y_nulls_un = self.z_nulls_un = None

        self.get_frames()

    def get_frames(self) -> None:
        '''ds'''

        self.x, self.y, self.z = split_data(self.port, self.filename, self.samples, self.number)

        self.find_nulls()

    def find_nulls(self) -> None:
        '''ds'''

        self.nulls_x_df = pd.DataFrame(np.zeros((2, int(self.number/3))), dtype = float)
        self.nulls_y_df = pd.DataFrame(np.zeros((2, int(self.number/3))), dtype = float)
        self.nulls_z_df = pd.DataFrame(np.zeros((2, int(self.number/3))), dtype = float)

        self.x_nulls = np.empty(int(self.number/3))
        self.y_nulls = np.empty(int(self.number/3))
        self.z_nulls = np.empty(int(self.number/3))
        self.x_stds = np.empty(int(self.number/3))
        self.y_stds = np.empty(int(self.number/3))
        self.z_stds = np.empty(int(self.number/3))

        for i in range(int(self.number/3)):
            mean_x_entry = np.mean(self.x[self.x.columns[i+1]])
            mean_y_entry = np.mean(self.y[self.y.columns[i+1]])
            mean_z_entry = np.mean(self.z[self.z.columns[i+1]])

            self.x_nulls[i] = mean_x_entry*self.vcc/self.bits
            self.y_nulls[i] = mean_y_entry*self.vcc/self.bits
            self.z_nulls[i] = mean_z_entry*self.vcc/self.bits
    
            self.x_stds[i] = np.std((self.x[self.x.columns[i+1]]), ddof=1)
            self.y_stds[i] = np.std((self.y[self.y.columns[i+1]]), ddof=1)
            self.z_stds[i] = np.std((self.z[self.z.columns[i+1]]), ddof=1)

        self.uncertainties_in_nulls()

    def uncertainties_in_nulls(self) -> None:
        '''ds'''

        self.x_nulls_un = np.empty(int(self.number/3))
        self.y_nulls_un = np.empty(int(self.number/3))
        self.z_nulls_un = np.empty(int(self.number/3))

        counts_absolute_uncertainty = 0.5
        uncetainty_in_vcc = (self.vcc_uncertainty/self.vcc)**2

        for i in range(int(self.number/3)):
            average_sensor_x = np.mean(self.x[self.x.columns[i+1]])
            average_sensor_y = np.mean(self.y[self.y.columns[i+1]])
            average_sensor_z = np.mean(self.z[self.z.columns[i+1]])

            reading_un_x = ((np.sqrt((counts_absolute_uncertainty)**2+(self.x_stds[i])**2))/average_sensor_x)**2
            reading_un_y = ((np.sqrt((counts_absolute_uncertainty)**2+(self.y_stds[i])**2))/average_sensor_y)**2
            reading_un_z = ((np.sqrt((counts_absolute_uncertainty)**2+(self.z_stds[i])**2))/average_sensor_z)**2

            self.x_nulls_un[i] = ((np.sqrt(reading_un_x+uncetainty_in_vcc))*self.x_nulls[i])
            self.y_nulls_un[i] = ((np.sqrt(reading_un_y+uncetainty_in_vcc))*self.y_nulls[i])
            self.z_nulls_un[i] = ((np.sqrt(reading_un_z+uncetainty_in_vcc))*self.z_nulls[i])

        self.saving_values()

    def saving_values(self) -> None:
        '''ds'''

        file_dir = (Path(__file__).parent / 'csv')
        output_nulls = file_dir/'nulls_and_uncertainties.csv'
        output_stds = file_dir/'stds.csv'

        with open(output_nulls, 'w', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.x_nulls)
            writer_obj.writerow(self.y_nulls)
            writer_obj.writerow(self.z_nulls)
            writer_obj.writerow(self.x_nulls_un)
            writer_obj.writerow(self.y_nulls_un)
            writer_obj.writerow(self.z_nulls_un)

        with open(output_stds, 'w', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.x_stds)
            writer_obj.writerow(self.y_stds)
            writer_obj.writerow(self.z_stds)

if __name__ == '__main__':
    x = Nulls(number = 6, port = '/dev/ttyUSB0', vcc = 5.0, filename = 'nulls_data.csv',
              vcc_un = 0.05, resolution = 10, samples = 400)
