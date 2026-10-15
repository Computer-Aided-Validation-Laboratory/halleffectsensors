from pathlib import Path
from csv import writer
import numpy as np
import pandas as pd
from func import split_data

class Sensitivities:
    '''ds'''

    def __init__(self, number: int, port: str, vcc: float, vcc_un: float, filename: str,
                 resolution: int, samples: int, calibration_field: np.array, field_abs_un: float):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.vcc_uncertainty = vcc_un
        self.filename = filename
        self.bits = (2**resolution)-1
        self.samples = samples
        self.calibration_field = calibration_field
        self.field_abs_uncertainty = field_abs_un

        self.sensor_uncertainty = 0.5
        self.uncertainty_in_vcc = (self.vcc_uncertainty/self.vcc)**2

        self.x_sens = np.empty(int(self.number/3))
        self.y_sens = np.empty(int(self.number/3))
        self.z_sens = np.empty(int(self.number/3))

        self.x_sens_un = np.empty(int(self.number/3))
        self.y_sens_un = np.empty(int(self.number/3))
        self.z_sens_un = np.empty(int(self.number/3))

        self.x = self.y = self.z = None
        self.x_nulls = self.y_nulls = self.z_nulls = None
        self.x_nulls_un = self.y_nulls_un = self.z_nulls_un = None
        self.x_stds = self.y_stds = self.z_stds = None

    def get_params(self) -> None:
        '''ds'''

        self.x, self.y, self.z = split_data(self.port, self.filename, self.samples, self.number)

        self.x_nulls = np.empty(int(self.number/3))
        self.y_nulls = np.empty(int(self.number/3))
        self.z_nulls = np.empty(int(self.number/3))

        self.x_nulls_un = np.empty(int(self.number/3))
        self.y_nulls_un = np.empty(int(self.number/3))
        self.z_nulls_un = np.empty(int(self.number/3))

        self.x_stds = np.empty(int(self.number/3))
        self.y_stds = np.empty(int(self.number/3))
        self.z_stds = np.empty(int(self.number/3))

        path_nulls_uncertainties = Path(__file__).parent / 'csv'
        parameters_df = pd.read_csv(path_nulls_uncertainties / 'nulls_and_uncertainties.csv', header = None)
        path_stds = Path(__file__).parent / 'csv'
        stds_df = pd.read_csv(path_stds / 'stds.csv', header = None)

        self.x_nulls = parameters_df.iloc[0].to_numpy()
        self.y_nulls = parameters_df.iloc[1].to_numpy()
        self.z_nulls = parameters_df.iloc[2].to_numpy()

        self.x_nulls_un = parameters_df.iloc[3].to_numpy()
        self.y_nulls_un = parameters_df.iloc[4].to_numpy()
        self.z_nulls_un = parameters_df.iloc[5].to_numpy()

        self.x_stds = stds_df.iloc[0].to_numpy()
        self.y_stds = stds_df.iloc[1].to_numpy()
        self.z_stds = stds_df.iloc[2].to_numpy()

        self.running()


    def current_comparison(self, current: float, current_abs_uncertainty: float, number_of_turns: int, coil_radius: float) -> None:
        '''just for when i want to use this, might not be for a while.'''

    def perform_calibration_x(self) -> None:
        '''ds'''
        x_data_un = self.x.copy()

        for i in range(int(self.number/3)):
            self.x[self.x.columns[i+1]] = self.x[self.x.columns[i+1]]*self.vcc/self.bits
            self.x[self.x.columns[i+1]] -= self.x_nulls[i]
            self.x_sens[i] = np.mean((self.x[self.x.columns[i+1]]/self.calibration_field[0])*1000)

            average_count = np.mean(x_data_un[x_data_un.columns[i+1]])
            count_uncertainty = ((np.sqrt(((self.sensor_uncertainty)**2)+(self.x_stds[i])**2))/average_count)**2
            average_voltage = np.mean((x_data_un[x_data_un.columns[i+1]])*self.vcc/self.bits)
            uncertainty_in_voltage = (average_voltage*(np.sqrt(count_uncertainty+self.uncertainty_in_vcc)))**2
            uncertainty_in_voltage_nulls = np.sqrt(uncertainty_in_voltage+(self.x_nulls_un[i])**2)
            x_data_un[x_data_un.columns[i+1]] *= self.vcc/self.bits
            x_data_un[x_data_un.columns[i+1]] = x_data_un[x_data_un.columns[i+1]]-self.x_nulls[i]
            total_null_uncertainty = (uncertainty_in_voltage_nulls/np.mean(x_data_un[x_data_un.columns[i+1]]))**2
            x_field_uncertainty = (self.field_abs_uncertainty/self.calibration_field[0])**2

            self.x_sens_un[i] = (np.sqrt(total_null_uncertainty+x_field_uncertainty))*self.x_sens[i]

        
    def perform_calibration_y(self) -> None:
        '''ds'''
        y_data_un = self.y.copy()

        for i in range(int(self.number/3)):
            self.y[self.y.columns[i+1]] = self.y[self.y.columns[i+1]]*self.vcc/self.bits
            self.y[self.y.columns[i+1]] -= self.y_nulls[i]
            self.y_sens[i] = np.mean((self.y[self.y.columns[i+1]]/self.calibration_field[1])*1000)

            average_count = np.mean(y_data_un[y_data_un.columns[i+1]])
            count_uncertainty = ((np.sqrt(((self.sensor_uncertainty)**2)+(self.y_stds[i])**2))/average_count)**2
            average_voltage = np.mean((y_data_un[y_data_un.columns[i+1]])*self.vcc/self.bits)
            uncertainty_in_voltage = (average_voltage*(np.sqrt(count_uncertainty+self.uncertainty_in_vcc)))**2
            uncertainty_in_voltage_nulls = np.sqrt(uncertainty_in_voltage+(self.y_nulls_un[i])**2)
            y_data_un[y_data_un.columns[i+1]] *= self.vcc/self.bits
            y_data_un[y_data_un.columns[i+1]] = y_data_un[y_data_un.columns[i+1]]-self.y_nulls[i]
            total_null_uncertainty = (uncertainty_in_voltage_nulls/np.mean(y_data_un[y_data_un.columns[i+1]]))**2
            y_field_uncertainty = (self.field_abs_uncertainty/self.calibration_field[1])**2

            self.y_sens_un[i] = (np.sqrt(total_null_uncertainty+y_field_uncertainty))*self.y_sens[i]


    def perform_calibration_z(self) -> None:
        '''ds'''
        z_data_un = self.z.copy()

        for i in range(int(self.number/3)):
            self.z[self.z.columns[i+1]] = self.z[self.z.columns[i+1]]*self.vcc/self.bits
            self.z[self.z.columns[i+1]] -= self.z_nulls[i]
            self.z_sens[i] = np.mean((self.z[self.z.columns[i+1]]/self.calibration_field[2])*1000)

            average_count = np.mean(z_data_un[z_data_un.columns[i+1]])
            count_uncertainty = ((np.sqrt(((self.sensor_uncertainty)**2)+(self.z_stds[i])**2))/average_count)**2
            average_voltage = np.mean((z_data_un[z_data_un.columns[i+1]])*self.vcc/self.bits)
            uncertainty_in_voltage = (average_voltage*(np.sqrt(count_uncertainty+self.uncertainty_in_vcc)))**2
            uncertainty_in_voltage_nulls = np.sqrt(uncertainty_in_voltage+(self.z_nulls_un[i])**2)
            z_data_un[z_data_un.columns[i+1]] *= self.vcc/self.bits
            z_data_un[z_data_un.columns[i+1]] = z_data_un[z_data_un.columns[i+1]]-self.z_nulls[i]
            total_null_uncertainty = (uncertainty_in_voltage_nulls/np.mean(z_data_un[z_data_un.columns[i+1]]))**2
            z_field_uncertainty = (self.field_abs_uncertainty/self.calibration_field[2])**2

            self.z_sens_un[i] = (np.sqrt(total_null_uncertainty+z_field_uncertainty))*self.z_sens[i]

    def saving_sens(self) -> None:
        '''ds'''

        file_dir = (Path(__file__).parent / 'csv')

        x_output_sen = file_dir / 'x_sens.csv'
        y_output_sen = file_dir / 'y_sens.csv'
        z_output_sen = file_dir / 'z_sens.csv'

        x_output_un = file_dir / 'x_uns.csv'
        y_output_un = file_dir / 'y_uns.csv'
        z_output_un = file_dir / 'z_uns.csv'

        with open(x_output_sen, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.x_sens)

        with open(y_output_sen, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.y_sens)

        with open(z_output_sen, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.z_sens)

        with open(x_output_un, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.x_sens_un)

        with open(y_output_un, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.y_sens_un)

        with open(z_output_un, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.z_sens_un)

    def running(self) -> None:
        '''ds'''

        self.get_params()

        if self.calibration_field[0] != 0:
            self.perform_calibration_x()
        if self.calibration_field[1] != 0:
            self.perform_calibration_y()
        if self.calibration_field[2] != 0:
            self.perform_calibration_z()

        self.saving_sens()

if __name__ == '__main__':
    x = Sensitivities(number = 6, port = '/dev/ttyUSB0', vcc = 5.0, vcc_un = 0.05,
                    filename = 'calibration_field_1.csv', resolution = 10,
                    samples = 400, calibration_field = [34,35,34], field_abs_un = 0.05)
