'''script that converts the data inputs to a magnetic field measurement'''
from pathlib import Path
import pandas as pd
import numpy as np
from func import split_data

class Fields:
    '''
    class for converting the raw data from the hall effect sensors into useful field strength
    measurements. takes the sensitivities and null voltages calculated during the calibration
    of the array and uses them. converts each direction of sensor individually to produce three
    data frames with field strength information for x, y, z fields.

    Attributes:
        number (int): number of sensors in array
        port (str): the computer port that the array is connected to
        filename (str): the name of the file that the data is stored under
        vcc (float): the vcc of the power source powering the sensor
        vcc_un (float): the uncertainty in the measurement of vcc of the power source
        resolution (int): the resolution (bit-depth) of the ADC used in the array
        samples (int): the number of samples for each measurement

    Methods:
        data_split() -> None:
            uses the `split_data` function to separate the incoming data being read from
            the sensor array into x, y and z directional data frames
        define() -> None:
            defines all the nulls/sens/uncertainties/stds variables that will be imported
            and saved from other classes
        get_params() -> None:
            gets the values of the variables defined in the previous method
        into_voltage() -> None:
            converts the incoming data into voltages by multiplying them by a scale factor
            and then subtracting the null voltage of each sensor from that sensors data. also
            tracks the uncertainties through this calculation
        field_strengths() -> None:
            converts the voltages into field strengths by multiplying each sensor by the
            previously calculated values for sensitivities for that sensor. also calculates
            the overall uncertainty in the field strength measurement
        house_keeping() -> None:
            customises the output data frames to make them easier to read, changes the column
            titles and converts the time into s from ms. displays the uncertainty in each
            measurement next to the field result
    '''
    def __init__(self, number: int, port: str, filename: str, vcc: float,
                 vcc_un: float, resolution: int, samples: int = 400):
        self.number = number
        self.port = port
        self.filename = filename
        self.vcc = vcc
        self.vcc_uncertainty = vcc_un
        self.bits = (2**resolution)-1
        self.samples = samples

        self.x_nulls = None
        self.y_nulls = None
        self.z_nulls = None

        self.x_nulls_un = None
        self.y_nulls_un = None
        self.z_nulls_un = None

        self.x_stds = None
        self.y_stds = None
        self.z_stds = None

        self.x_sens = None
        self.y_sens = None
        self.z_sens = None

        self.x_sens_un = None
        self.y_sens_un = None
        self.z_sens_un = None

        self.x = None
        self.y = None
        self.z = None

        self.x_sensor_uncertainty = None
        self.y_sensor_uncertainty = None
        self.z_sensor_uncertainty = None

        self.x_voltage_un = None
        self.y_voltage_un = None
        self.z_voltage_un = None

        self.x_field_un = None
        self.y_field_un = None
        self.z_field_un = None

        self.x_sensors = None
        self.y_sensors = None
        self.z_sensors = None

        self.data_split()

    def data_split(self) -> None:
        '''
        uses the `split_data` function to separate the incoming data being read from
        the sensor array into x, y and z directional data frames
        Args:
            None
        Returns:
            None
        '''

        self.x, self.y, self.z, self.x_sensors, self.y_sensors, self.z_sensors = split_data(self.port, self.filename, self.samples, self.number)

        self.define()


    def define(self) -> None:
        '''
        defines all the nulls/sens/uncertainties/stds variables that will be imported
        and saved from other classes
        Args:
            None
        Retruns:
            None        
        '''

        self.x_nulls = np.empty(self.x_sensors)
        self.y_nulls = np.empty(self.y_sensors)
        self.z_nulls = np.empty(self.z_sensors)

        self.x_nulls_un = np.empty(self.x_sensors)
        self.y_nulls_un = np.empty(self.y_sensors)
        self.z_nulls_un = np.empty(self.z_sensors)

        self.x_stds = np.empty(self.x_sensors)
        self.y_stds = np.empty(self.y_sensors)
        self.z_stds = np.empty(self.z_sensors)

        self.x_sens = np.empty(self.x_sensors)
        self.y_sens = np.empty(self.y_sensors)
        self.z_sens = np.empty(self.z_sensors)

        self.x_sens_un = np.empty(self.x_sensors)
        self.y_sens_un = np.empty(self.y_sensors)
        self.z_sens_un = np.empty(self.z_sensors)

        self.get_params()

    def get_params(self) -> None:
        '''
        gets the values of the variables defined in the previous method
        Args:
            None
        Returns:
            None
        '''

        csv_folder_path = Path(__file__).parent / 'csv'
        nulls_and_uncertainties_df = pd.read_csv(csv_folder_path/'nulls_and_uncertainties.csv',
                                                 header = None)

        self.x_nulls = nulls_and_uncertainties_df.iloc[0].to_numpy()
        self.y_nulls = nulls_and_uncertainties_df.iloc[1].to_numpy()
        self.z_nulls = nulls_and_uncertainties_df.iloc[2].to_numpy()

        self.x_nulls_un = nulls_and_uncertainties_df.iloc[3].to_numpy()
        self.y_nulls_un = nulls_and_uncertainties_df.iloc[4].to_numpy()
        self.z_nulls_un = nulls_and_uncertainties_df.iloc[5].to_numpy()

        stds_df = pd.read_csv(csv_folder_path / 'stds.csv', header = None)

        self.x_stds = stds_df.iloc[0]
        self.y_stds = stds_df.iloc[1]
        self.z_stds = stds_df.iloc[2]

        x_sens_df = pd.read_csv(csv_folder_path / 'x_sens.csv', header = None)
        y_sens_df = pd.read_csv(csv_folder_path / 'y_sens.csv', header = None)
        z_sens_df = pd.read_csv(csv_folder_path / 'z_sens.csv', header = None)

        x_sens_un_df = pd.read_csv(csv_folder_path / 'x_uns.csv', header = None)
        y_sens_un_df = pd.read_csv(csv_folder_path / 'y_uns.csv', header = None)
        z_sens_un_df = pd.read_csv(csv_folder_path / 'z_uns.csv', header = None)

        for i in range(self.x_sensors):
            self.x_sens[i] = np.mean(x_sens_df[x_sens_df.columns[i]])
            self.x_sens_un[i] = np.mean(x_sens_un_df[x_sens_un_df.columns[i]])

        for i in range(self.y_sensors):
            self.y_sens[i] = np.mean(y_sens_df[y_sens_df.columns[i]])
            self.y_sens_un[i] = np.mean(y_sens_un_df[y_sens_un_df.columns[i]])

        for i in range(self.z_sensors):
            self.z_sens[i] = np.mean(z_sens_df[z_sens_df.columns[i]])
            self.z_sens_un[i] = np.mean(z_sens_un_df[z_sens_un_df.columns[i]])

        self.into_voltage()

    def into_voltage(self) -> None:
        '''
        converts the incoming data into voltages by multiplying them by a scale factor
        and then subtracting the null voltage of each sensor from that sensors data. also
        tracks the uncertainties through this calculation
        Args:
            None
        Returns:
            None
        '''

        self.x_voltage_un = np.empty(self.x_sensors)
        self.y_voltage_un = np.empty(self.y_sensors)
        self.z_voltage_un = np.empty(self.z_sensors)

        for i in range(self.x_sensors):
            self.x_sensor_uncertainty = np.sqrt((0.5**2)+self.x_stds[i])
            x_average_reading = np.mean(self.x[self.x.columns[i+1]])

            self.x[self.x.columns[i+1]] = self.x[self.x.columns[i+1]]*self.vcc/self.bits

            x_average_voltage = np.mean(self.x[self.x.columns[i+1]])
            x_reading_un = (self.x_sensor_uncertainty/x_average_reading)**2
            x_vcc_uncertainty = (self.vcc_uncertainty/self.vcc)**2
            x_uncertainty_in_voltage = x_average_voltage*np.sqrt(x_reading_un+x_vcc_uncertainty)

            self.x[self.x.columns[i+1]] = self.x[self.x.columns[i+1]]-self.x_nulls[i]

            self.x_voltage_un[i] = np.sqrt((self.x_nulls_un[i]**2)+(x_uncertainty_in_voltage**2))

        for i in range(self.y_sensors):
            self.y_sensor_uncertainty = np.sqrt((0.5**2)+self.y_stds[i])
            y_average_reading = np.mean(self.y[self.y.columns[i+1]])

            self.y[self.y.columns[i+1]] = self.y[self.y.columns[i+1]]*self.vcc/self.bits

            y_average_voltage = np.mean(self.y[self.y.columns[i+1]])
            y_reading_un = (self.y_sensor_uncertainty/y_average_reading)**2
            y_vcc_uncertainty = (self.vcc_uncertainty/self.vcc)**2
            y_uncertainty_in_voltage = y_average_voltage*np.sqrt(y_reading_un+y_vcc_uncertainty)

            self.y[self.y.columns[i+1]] = self.y[self.y.columns[i+1]]-self.y_nulls[i]

            self.y_voltage_un[i] = np.sqrt((self.y_nulls_un[i]**2)+(y_uncertainty_in_voltage**2))

        for i in range(self.z_sensors):
            self.z_sensor_uncertainty = np.sqrt((0.5**2)+self.z_stds[i])
            z_average_reading = np.mean(self.z[self.z.columns[i+1]])

            self.z[self.z.columns[i+1]] = self.z[self.z.columns[i+1]]*self.vcc/self.bits

            z_average_voltage = np.mean(self.z[self.z.columns[i+1]])
            z_reading_un = (self.z_sensor_uncertainty/z_average_reading)**2
            z_vcc_uncertainty = (self.vcc_uncertainty/self.vcc)**2
            z_uncertainty_in_voltage = z_average_voltage*np.sqrt(z_reading_un+z_vcc_uncertainty)

            self.z[self.z.columns[i+1]] = self.z[self.z.columns[i+1]]-self.z_nulls[i]

            self.z_voltage_un[i] = np.sqrt((self.z_nulls_un[i]**2)+(z_uncertainty_in_voltage**2))

        self.field_strengths()

    def field_strengths(self) -> None:
        '''
        converts the voltages into field strengths by multiplying each sensor by the
        previously calculated values for sensitivities for that sensor. also calculates
        the overall uncertainty in the field strength measurement
        Args:
            None
        Returns:
            None
        '''

        self.x_field_un = np.empty(self.x_sensors)
        self.y_field_un = np.empty(self.y_sensors)
        self.z_field_un = np.empty(self.z_sensors)

        for i in range(self.x_sensors):
            x_voltage_un = (np.mean(self.x_voltage_un[i]/self.x[self.x.columns[i+1]]))**2

            self.x[self.x.columns[i+1]] = self.x[self.x.columns[i+1]]/self.x_sens[i]

            x_average_field = np.mean(self.x[self.x.columns[i+1]])
            x_sens_un = (self.x_sens_un[i]/np.mean(self.x_sens))**2
            self.x_field_un[i] = x_average_field*(np.sqrt((x_sens_un)+(x_voltage_un)))

        for i in range(self.y_sensors):
            y_voltage_un = (np.mean(self.y_voltage_un[i]/self.y[self.y.columns[i+1]]))**2

            self.y[self.y.columns[i+1]] = self.y[self.y.columns[i+1]]/self.y_sens[i]

            y_average_field = np.mean(self.y[self.y.columns[i+1]])
            y_sens_un = (self.y_sens_un[i]/np.mean(self.y_sens))**2
            self.y_field_un[i] = y_average_field*(np.sqrt((y_sens_un)+(y_voltage_un)))

        for i in range(self.z_sensors):
            z_voltage_un = (np.mean(self.y_voltage_un[i]/self.y[self.y.columns[i+1]]))**2

            self.z[self.z.columns[i+1]] = self.z[self.z.columns[i+1]]/self.z_sens[i]

            z_average_field = np.mean(self.z[self.z.columns[i+1]])
            z_sens_un = (self.z_sens_un[i]/np.mean(self.z_sens))**2
            self.z_field_un[i] = z_average_field*(np.sqrt((z_voltage_un)+(z_sens_un)))

        self.house_keeping()

    def house_keeping(self) -> None:
        '''
        customises the output data frames to make them easier to read, changes the column
        titles and converts the time into s from ms. displays the uncertainty in each
        measurement next to the field result
        Args:
            None
        Returns:
            None
        '''

        x_new_cols = ['time/s']
        x_new_cols.extend([f'field_strength_S{i}/mT' for i in range(1, self.x_sensors+1)])

        y_new_cols = ['time/s']
        y_new_cols.extend([f'field_strength_S{i}/mT' for i in range(1, self.y_sensors+1)])

        z_new_cols = ['time/s']
        z_new_cols.extend([f'field_strength_S{i}/mT' for i in range(1, self.z_sensors+1)])

        self.x.columns = x_new_cols
        self.y.columns = y_new_cols
        self.z.columns = z_new_cols

        self.x[self.x.columns[0]] = (self.x[self.x.columns[0]].astype(float))/1000
        self.y[self.y.columns[0]] = (self.y[self.y.columns[0]].astype(float))/1000
        self.z[self.z.columns[0]] = (self.z[self.z.columns[0]].astype(float))/1000

        x_relative_uncertainty = np.empty(self.x_sensors)
        y_relative_uncertainty = np.empty(self.y_sensors)
        z_relative_uncertainty = np.empty(self.z_sensors)

        for i in range(self.x_sensors):
            x_column = self.x.columns[i+1]
            x_relative_uncertainty[i] = self.x_field_un[i]
            self.x[x_column] = self.x[x_column].apply(lambda x: f'{x:.3f} ± {abs(x*x_relative_uncertainty[i]):.3f}')

        for i in range(self.y_sensors):
            y_column = self.y.columns[i+1]
            y_relative_uncertainty[i] = self.y_field_un[i]
            self.y[y_column] = self.y[y_column].apply(lambda x: f'{x:.3f} ± {abs(x*y_relative_uncertainty[i]):.3f}')

        for i in  range(self.z_sensors):
            z_column = self.z.columns[i+1]
            z_relative_uncertainty[i] = self.z_field_un[i]
            self.z[z_column] = self.z[z_column].apply(lambda x: f'{x:.3f} ± {abs(x*z_relative_uncertainty[i]):.3f}')

        print(self.x)
        print(self.y)
        print(self.z)

if __name__ == '__main__':
    x = Fields(number = 6, port = '/dev/ttyUSB0', filename = 'test_1.csv',
               vcc = 5.0, vcc_un = 0.05, resolution = 10, samples = 400)
