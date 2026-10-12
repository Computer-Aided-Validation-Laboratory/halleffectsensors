''' second part of the calibration code, along with the nulls.py. This script calculates
the sensitivity (scale factor between voltage and field strength) of each sensor and 
the associates uncertainties with each calculation'''

from pathlib import Path
from csv import writer
import numpy as np
import pandas as pd
from read import read_data

class Sensitivity:
    '''
    class for calculating the sensitivity of each sensor and its uncertainty. takes input
    of a known field value and scales up the outputted voltage correctly. Also has a method
    for comparing the field created by the hemlholtz coil as measured by the magnetic field
    probe and what field should be produced based on the current being fed through the coil,
    the radius of the coils and the number of turns present in the coil. saves the values
    for sensitivity for each sensor to be used as scale factors in data conversion.

    Attributes:
        number (int): the number of sensors present in the sensor array
        port (str): the computer port that the Arduino is connected to (which port needs to be
            read from)
        vcc (float): the value of the VCC (input voltage) from the Arduino/external power supply
        vcc_un (float): the associated uncertainty with the value obtained for the VCC
        filename (str): the filename where the data from the sensors is read into
        bits (int): the bit depth of the analogue-digital converter (ADC)
        samples (int): the number of samples taken and used for these calculations
        calibration_field (float): the value of the field that the sensor array is being
            calibrated against
        field_uncertainty (float): the uncertainty in the measurement of the field that the sensors
            are calibrated against
        
    Methods:
        get_parameters() -> None:
            imports and saves the parameters found during calibration (null voltages
            and uncertainties for each sensor in the array) found so far.
        current_comparison(current: float, current_uncertainty: float, number_of_turns: int,
        radius_of_coils: float) -> None:
            calculates what the theoretical field value should be based on the current sent through
            the coil, the radius of the coil and the number of turns in the coil
        perform_calibration() -> None:
            calculates the scale factor required to get from the voltage value outputted into the
            value of the known calibration field with its uncertainty
        saves_sens() -> None:
            saves the values calculated for the sensitivity of each sensor and the uncertainty in
            sensitivity for each sensor in csv files so that they can be accessed later. the csv
            files are appended each time the class is run (for different calibration field values)
    '''

    def __init__(self, number: int, port: str, vcc: float, vcc_un: float, filename: str,
                bits: int, samples: int, calibration_field: float, field_uncertainty: float):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.vcc_uncertainty = vcc_un
        self.filename = filename
        self.bits = (2**bits)-1
        self.samples = samples
        self.field = calibration_field
        self.field_uncertainty = field_uncertainty

        self.calibration_data = None
        self.nulls = None
        self.nulls_uncertainties = None
        self.stds = None
        self.sens_frame = None
        self.sens_uncertainties_frame = None
        self.sensitivities = None
        self.uncertainty_in_sens = None

        self.get_parameters()

    def get_parameters(self) -> None:
        '''
        gets the parameters calculated in the first part of the calibration
        software and stores them as variables that can be used in the
        rest of the class
        Args:
            None
        Returns:
            None
        '''

        self.nulls = np.empty(self.number)
        self.nulls_uncertainties = np.empty(self.number)
        self.stds = np.empty(self.number)

        path_nulls = Path(__file__).resolve().with_name('nulls.csv')
        parameters_df = pd.read_csv(path_nulls)

        path_stds = Path(__file__).resolve().with_name('stds.csv')
        stds_df = pd.read_csv(path_stds)

        self.nulls = parameters_df.iloc[0].to_numpy()
        self.nulls_uncertainties = parameters_df.iloc[1].to_numpy()
        self.stds = stds_df.iloc[0].to_numpy()

    def current_comparison(self, current: float, current_uncertainty: float, number_of_turns: int, coil_radius: float) -> None:
        '''
        takes inputs for the current, current uncertainty, the number of turns
        and the radius of the coils to calculate the theoretical field value
        and compares to the actual field value produced and measured with
        a magnetic field probe
        Args;
            current (float): current passed into the coils (helmholtz)
            current_uncertainty (float): uncertainty in measurement of current
                being passed through the Helmholtz coil
            number_of_turns (int): the number of turns in the calibration coil
            coil_radius (float): radius of calibration coils
        Returns:
            None
        '''

        theoretical_field = (0.8**1.5)*(4*np.pi*(10**(-7)))*(number_of_turns*current)/coil_radius

        square = (((current_uncertainty/current)**2)+((0.5*10**(-3)/coil_radius)**2))
        self.field_uncertainty = np.sqrt(square)                  *theoretical_field

        difference = (np.abs(theoretical_field-self.field))/self.field*100
        print(f'the % difference in theoretical and measured field is {difference}%')

        self.perform_calibration()

    def perform_calibration(self) -> None:
        '''
        finds the value for the sensitivity for each sensor in the array.
        caluclates the uncertainty assciated with each value as it goes.
        Args:
            None
        Returns:
            None
        '''
        
        uncertainty_in_sensor = 0.5
        
        self.calibration_data = read_data(self.port, self.filename, self.samples)
        uncertainty_sen_frame = self.calibration_data
        
        self.sensitivities = [0]*self.number
        self.uncertainty_in_sens = [0]*self.number
        
        vcc_uncertainty = (self.vcc_uncertainty/self.vcc)**2

        for x in range(self.number):
        
            average_sen_data = uncertainty_sen_frame[uncertainty_sen_frame.columns[x+1]].mean()
            reading_uncertainty = ((np.sqrt(((uncertainty_in_sensor)**2)+(self.stds[x])**2))/average_sen_data)**2
            rooted = np.sqrt(reading_uncertainty+vcc_uncertainty)
        
            average_voltage_value = (self.calibration_data[self.calibration_data.columns[x+1]]*self.vcc/self.bits).mean()
        
            uncertainty_in_volt = rooted*average_voltage_value
            uncertainty_in_volt_nulls = (np.sqrt(((uncertainty_in_volt)**2)+((self.nulls_uncertainties[x])**2)))
        
            self.calibration_data[self.calibration_data.columns[x+1]] = self.calibration_data[self.calibration_data.columns[x+1]]*self.vcc / self.bits
            self.calibration_data[self.calibration_data.columns[x+1]] -= self.nulls[x]
        
            third = ((uncertainty_in_volt_nulls)/(self.calibration_data[self.calibration_data.columns[x+1]].mean()))**2
            fourth = ((self.field_uncertainty)/self.field)**2
            rooted2 = np.sqrt(third+fourth)
        
            self.sensitivities[x] = ((self.calibration_data[self.calibration_data.columns[x+1]].mean())/self.field)*1000
            self.uncertainty_in_sens[x] = rooted2*self.sensitivities[x]

        self.saves_sens()

    def saves_sens(self) -> None:
        '''
        saves the values just calculats in a csv file so that they can be used
        as a scale factor in data conversion
        Args:
            None
        Returns:
            None
        '''
        path = Path(__file__).parent
        output1 = path/'sens.csv'
        output2 = path/'uncertainties.csv'

        with open(output1, 'a', encoding ='utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.sensitivities)

        with open(output2, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.uncertainty_in_sens)
