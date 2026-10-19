'''script that calculates the null voltages and noise of each sensor'''
from pathlib import Path
from csv import writer
import numpy as np
import pandas as pd
from func import split_data


class Nulls:
    '''
    class to calculate the null voltage and the associated uncertainties of each sensor in the
    array. also calculates the standard deviations for each sensor. the data is split directionally 
    by the imported function `split_data`.

    Attributes
        number (int): the number of sensors present in the array (total for all directions)
        port (str): the computer port that the array connects to
        vcc (float): the vcc of the Arduino (voltage into array)
        filename (str): filename that the recorded data is stored under
        vcc_un (float): the uncertainty in the measurement of vcc
        resolution (int): the resolution of the ADC that is used
        samples (int): the number of samples taken in each measurement

    Methods:
        get_frames() -> None: 
            splits the incoming data into x, y and z data frames by using the imported function
        find_nulls() -> None:
            calculates the null voltages for each sensor in each data frame and stores them. also
            calculates the standard deviations for each sensor and stores them
        uncertainties_in_nulls() -> None:
            calculates the associated uncertainties with each null voltage calculation
        saving_values() -> None:
            saves the values calculated in this class in csvs so that they can be used later on

    '''

    def __init__(self, number: int, port: str, vcc: float, filename: str,
                 vcc_un: float, resolution: int, samples: int = 400):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.filename = filename
        self.vcc_uncertainty = vcc_un
        self.bits = (2**resolution)-1
        self.samples = samples

        self.x = None
        self.y = None
        self.z = None

        self.nulls_x_df = None
        self.nulls_y_df = None
        self.nulls_z_df = None

        self.x_stds = None
        self.y_stds = None
        self.z_stds = None

        self.x_nulls = None
        self.y_nulls = None
        self.z_nulls = None

        self.x_nulls_un = None
        self.y_nulls_un = None
        self.z_nulls_un = None

        self.x_sensors = None
        self.y_sensors = None
        self.z_sensors = None

        self.get_frames()

    def get_frames(self) -> None:
        '''
        method that calls the data splitting function `split_data` and saves the 
        directional data frames to be used throughout this class.
        Args:
            None
        Returns:
            None
        '''

        self.x, self.y, self.z, self.x_sensors, self.y_sensors, self.z_sensors = split_data(self.port, self.filename, self.samples, self.number)
        print(self.x)
        self.find_nulls()

    def find_nulls(self) -> None:
        '''
        method for calculating the null voltages of each sensor and the standard deviation
        at the same time. stores the answers in different numpy arrays
        Args:
            None
        Returns:
            None
        '''

        self.nulls_x_df = pd.DataFrame(np.zeros((2, self.x_sensors)), dtype = float)
        self.nulls_y_df = pd.DataFrame(np.zeros((2, self.y_sensors)), dtype = float)
        self.nulls_z_df = pd.DataFrame(np.zeros((2, self.z_sensors)), dtype = float)

        self.x_nulls = np.empty(self.x_sensors)
        self.y_nulls = np.empty(self.y_sensors)
        self.z_nulls = np.empty(self.z_sensors)

        self.x_stds = np.empty(self.x_sensors)
        self.y_stds = np.empty(self.y_sensors)
        self.z_stds = np.empty(self.z_sensors)

        for i in range(self.x_sensors):
            mean_x_entry = np.mean(self.x[self.x.columns[i+1]])
            self.x_nulls[i] = mean_x_entry*self.vcc/self.bits
            self.x_stds[i] = np.std((self.x[self.x.columns[i+1]]), ddof=1)

        for i in range(self.y_sensors):
            mean_y_entry = np.mean(self.y[self.y.columns[i+1]])
            self.y_nulls[i] = mean_y_entry*self.vcc/self.bits
            self.y_stds[i] = np.std((self.y[self.y.columns[i+1]]), ddof=1)

        for i in range(self.z_sensors):
            mean_z_entry = np.mean(self.z[self.z.columns[i+1]])
            self.z_nulls[i] = mean_z_entry*self.vcc/self.bits
            self.z_stds[i] = np.std((self.z[self.z.columns[i+1]]), ddof=1)

        self.uncertainties_in_nulls()

    def uncertainties_in_nulls(self) -> None:
        '''
        method for calculating the uncertainty in the null voltage of each sensor in the array
        and stores the values
        Args:
            None
        Returns:
            None
        '''

        self.x_nulls_un = np.empty(self.x_sensors)
        self.y_nulls_un = np.empty(self.y_sensors)
        self.z_nulls_un = np.empty(self.z_sensors)

        counts_absolute_uncertainty = 0.5
        uncetainty_in_vcc = (self.vcc_uncertainty/self.vcc)**2

        for i in range(self.x_sensors):
            average_sensor_x = np.mean(self.x[self.x.columns[i+1]])
            reading_un_x = ((np.sqrt((counts_absolute_uncertainty)**2+(self.x_stds[i])**2))/average_sensor_x)**2
            self.x_nulls_un[i] = ((np.sqrt(reading_un_x+uncetainty_in_vcc))*self.x_nulls[i])

        for i in range(self.y_sensors):
            average_sensor_y = np.mean(self.y[self.y.columns[i+1]])
            reading_un_y = ((np.sqrt((counts_absolute_uncertainty)**2+(self.y_stds[i])**2))/average_sensor_y)**2
            self.y_nulls_un[i] = ((np.sqrt(reading_un_y+uncetainty_in_vcc))*self.y_nulls[i])

        for i in range(self.z_sensors):
            average_sensor_z = np.mean(self.z[self.z.columns[i+1]])
            reading_un_z = ((np.sqrt((counts_absolute_uncertainty)**2+(self.z_stds[i])**2))/average_sensor_z)**2
            self.z_nulls_un[i] = ((np.sqrt(reading_un_z+uncetainty_in_vcc))*self.z_nulls[i])

        self.saving_values()

    def saving_values(self) -> None:
        '''
        method for saving the values calculated in this class to csvs
        so that they can be used in other scripts for calibration or for
        conversion
        Args:
            None
        Returns:
            None
        '''

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
    x = Nulls(number = 9, port = '/dev/ttyUSB0', vcc = 5.0, filename = 'nulls_data.csv',
              vcc_un = 0.05, resolution = 10, samples = 400)

# need to change split_data to work for x, y and z having different amounts of sensors