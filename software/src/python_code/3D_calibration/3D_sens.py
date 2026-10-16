'''script that calculates the sensitivities of each sensor in the array'''
from pathlib import Path
from csv import writer
import numpy as np
import pandas as pd
from func import split_data

class Sensitivities:
    '''
    class for calibrating the sensors in a magnetic field. this calculates the
    sensitivity of each sensor in the array by comparing it to the field that 
    correlates to the direction the sensor is pointing. also calculates the associated
    uncertainty with each calculation. these values are stored similarly to in the
    Nulls class.

    Attributes:
        number (int): the number of sensors in the array
        port (str): the computer port that the sensor array is connected to
        vcc (float): the vcc of the power source powering the sensor array
        vcc_un (float): the uncertainty in the vcc measurement
        filename (str): the filename the calibration data is stored under
        resolution (int): the resolution of the ADC used in the circuit
        samples (int): the number of samples collected in each measurement
        calibration_field (np.array): the field that the sensors are calibrated
            against
        field_abs_un (float): the uncertainty in the measurement of the value of the
            calibration field

    Methods:
        get_params() -> None: 
            imports values calculated in other scripts like the null voltages, the
            noise of each sensor (std) and the uncertainties in each measurement and
            saves them as arrays to be used in this class
        current_comparison() -> None:
            takes inputs for the coil properties and calculates what the outputted
            magnetic field should be so that it can be compared to what is detected
            by the probe.
        perform_calibration_x() -> None:
            calibrates all the directionally 'x' sensors in the array against the x
            calibration field.
        perform_calibration_y() -> None:
            calibrates all the directionally 'y' sensors in the array against the y
            calibration field.
        perform_calibration_z() -> None:
            calibrates all the directionally 'z' sensors in the array against the z
            calibration field.        
    '''

    def __init__(self, number: int, port: str, vcc: float, vcc_un: float, filename: str, resolution: int,
                samples: int, calibration_field: np.array, field_abs_un: float, inputs: bool = False):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.vcc_uncertainty = vcc_un
        self.filename = filename
        self.bits = (2**resolution)-1
        self.samples = samples
        self.calibration_field = calibration_field
        self.field_abs_uncertainty = field_abs_un
        self.inputs = inputs

        self.sensor_uncertainty = 0.5
        self.uncertainty_in_vcc = (self.vcc_uncertainty/self.vcc)**2

        self.x_sens = None
        self.y_sens = None
        self.z_sens = None

        self.x_sens_un = None
        self.y_sens_un = None
        self.z_sens_un = None

        self.x = None
        self.y = None
        self.z = None

        self.x_nulls = None
        self.y_nulls = None
        self.z_nulls = None

        self.x_nulls_un = None
        self.y_nulls_un = None
        self.z_nulls_un = None

        self.x_stds = None
        self.y_stds = None
        self.z_stds = None

        self.x_sensors = None
        self.y_sensors = None
        self.z_sensors = None

    def get_params(self) -> None:
        '''
        imports values calculated in other scripts like the null voltages, the
        noise of each sensor (std) and the uncertainties in each measurement and
        saves them as arrays to be used in this class.
        Args:
            None
        Returns:
            None
        '''

        self.x, self.y, self.z, self.x_sensors, self.y_sensors, self.z_sensors = split_data(self.port, self.filename, self.samples, self.number)

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

        self.get_params()

    def current_comparison(self, current: np.array, current_abs_uncertainty: float,
                           number_of_turns: int, coil_radius: float) -> None:
        '''
        takes inputs for the coil properties and calculates what the outputted
        magnetic field should be so that it can be compared to what is detected
        by the probe.
        Args:
            current (np.array): input current into the calibration coils
            current_abs_uncertainty (float): uncertainty in the measurement of
                the current into the coils
            number_of_turns (int): the number of turns in the calibration coils
            coil_radius (float): the radius of the coils used for calibration
        Returns:
            None
        '''

        x_expected_field = (0.8**1.5)*(4*np.pi*(10**(-7)))*(number_of_turns*current[0])/coil_radius
        x_square = ((current_abs_uncertainty/current[0])**2)+((0.5*10**(-3)/coil_radius)**2)
        x_field_uncertainty = np.sqrt(x_square)*x_expected_field
        x_diff = (np.abs(x_expected_field-self.calibration_field[0]))/self.calibration_field[0]*100
        print(f'expected field (x):{x_expected_field} ± {x_field_uncertainty}, actual field (x): {self.calibration_field[0]}')
        print(f'% difference: {x_diff}')

        y_expected_field = (0.8**1.5)*(4*np.pi*(10**(-7)))*(number_of_turns*current[1])/coil_radius
        y_square = ((current_abs_uncertainty/current[1])**2)+((0.5*10**(-3)/coil_radius)**2)
        y_field_uncertainty = np.sqrt(y_square)*y_expected_field
        y_diff = (np.abs(y_expected_field-self.calibration_field[1]))/self.calibration_field[1]*100
        print(f'expected field (y):{y_expected_field} ± {y_field_uncertainty}, actual field (y): {self.calibration_field[1]}')
        print(f'% difference: {y_diff}')

        z_expected_field = (0.8**1.5)*(4*np.pi*(10**(-7)))*(number_of_turns*current[2])/coil_radius
        z_square = ((current_abs_uncertainty/current[2])**2)+((0.5*10**(-3)/coil_radius)**2)
        z_field_uncertainty = np.sqrt(z_square)*z_expected_field
        z_diff = (np.abs(z_expected_field-self.calibration_field[2]))/self.calibration_field[2]*100
        print(f'expected field (z):{z_expected_field} ± {z_field_uncertainty}, actual field (z): {self.calibration_field[2]}')
        print(f'% difference: {z_diff}')

        if self.calibration_field[0] != 0:
            self.perform_calibration_x()
        if self.calibration_field[1] != 0:
            self.perform_calibration_y()
        if self.calibration_field[2] != 0:
            self.perform_calibration_z()

        self.saving_sens()

    def perform_calibration_x(self) -> None:
        '''
        calibrates all the directionally 'x' sensors in the array against the x
        calibration field. this is done by calculating the sensitivity of each sensor
        and the associated uncertainty with each measurement.
        Args:
            None
        Returns:
            None
        '''
        x_data_un = self.x.copy()

        for i in range(self.x_sensors):
            self.x[self.x.columns[i+1]] = self.x[self.x.columns[i+1]]*self.vcc/self.bits
            self.x[self.x.columns[i+1]] -= self.x_nulls[i]
            self.x_sens[i] = np.mean((self.x[self.x.columns[i+1]]/self.calibration_field[0])*1000000)

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
        '''
        calibrates all the directionally 'y' sensors in the array against the y
        calibration field. this is done by calculating the sensitivity of each sensor
        and the associated uncertainty with each measurement.
        Args:
            None
        Returns:
            None        
        '''
        y_data_un = self.y.copy()

        for i in range(self.y_sensors):
            self.y[self.y.columns[i+1]] = self.y[self.y.columns[i+1]]*self.vcc/self.bits
            self.y[self.y.columns[i+1]] -= self.y_nulls[i]
            self.y_sens[i] = np.mean((self.y[self.y.columns[i+1]]/self.calibration_field[1])*1000000)

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
        '''
        calibrates all the directionally 'z' sensors in the array against the z
        calibration field. this is done by calculating the sensitivity of each sensor
        and the associated uncertainty with each measurement.
        Args:
            None
        Returns:
            None        
        '''
        z_data_un = self.z.copy()

        for i in range(self.z_sensors):
            self.z[self.z.columns[i+1]] = self.z[self.z.columns[i+1]]*self.vcc/self.bits
            self.z[self.z.columns[i+1]] -= self.z_nulls[i]
            self.z_sens[i] = np.mean((self.z[self.z.columns[i+1]]/self.calibration_field[2])*1000000)

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
        '''
        method that saves the calculated values of sensitivity and uncertainty in csvs so that 
        they can be used in the conversion script. they are saved in csvs in a separate folder
        to the code, in their own folder called 'csv'
        Args:
            None
        Returns:
            None
        '''

        file_dir = Path(__file__).parent / 'csv'

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


if __name__ == '__main__':
    x = Sensitivities(number = 6, port = '/dev/ttyUSB0', vcc = 5.0, vcc_un = 0.05,
                    filename = 'calibration_field_1.csv', resolution = 10,
                    samples = 400, calibration_field = [34,35,34], field_abs_un = 0.05)
    x.current_comparison(current=[2,2,2], current_abs_uncertainty=0.05,
                         number_of_turns=50, coil_radius=2)
