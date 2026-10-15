'''contains the class that converts the sensor output into field strengths and uncertanties'''

from pathlib import Path
import pandas as pd
import numpy as np
from read import read_data

class Conversion:
    '''
    class for converting the raw data read from the hall effect sensors and the Arduino into useful data 
    (field strengths for each sensor and time stamps). Uses the null voltage and sensitivity values 
    calulated during the calibration steps. Calculates the uncertainty in each field measurement

    Attributes:
        port (str): the port of the computer that the arduino/hall effect sensor array is plugged in to
        filename (str): the name of the csv file that stores the data being read - is converted to a 
            pandas dataframe for easier manipulation
        number (int): the number of sensors in the array - provides information for how many iterations 
            are required
        vcc (float): the VCC (voltage output) of the arduino into the sensors
        vcc_un (float): the associated uncertainty with the value of the VCC
        samples (int): the number of data samples taken 
    
    Methods:
        get_params() -> None: 
            reads the csvs file where the calibration parameters (null voltages/sensitivity/uncertainties)
            are stored and saves them as arrays so that they can be used in this class for the conversion
        into_voltage() -> None: 
            multiplies the numbers outputted by the sensors to convert them into voltages,
            and subtracts the null voltage for each sensor off of that sensors readings. Calculates the 
            uncertainty in the voltage at this stage for each sensor
        field_strengths() -> pd.DataFrame: 
            converts the voltages into field strengths by dividing by the sensitivity and calculates the
            associated uncertainty with each field measurement. renames the dataframe headings
        display_uncertainty() -> None: 
            uses the calculated fractional uncertainty and applies it to each value of the field, displays
            them in the output dataframe
        run() -> None: 
            method for running the other methods in the class
    '''

    def __init__(self, port: str, filename: str, number: int, vcc: float, vcc_un: float, bits: int, samples: int = 200):
        self.port = port
        self.filename = filename
        self.number = number
        self.vcc = vcc
        self.vcc_un = vcc_un
        self.bits = (2**bits)-1
        self.samples = samples

        self.nulls = None
        self.sensitivities = None
        self.data = None
        self.nulls_uncertainties = None
        self.sensitivities_uncertainties = None
        self.stds = None
        self.sensor_uncertainty = None
        self.voltage_uncertainty = None
        self.field_uncertainty = None

        self.run()

    def get_params(self) -> None:
        '''
        initialises variables for null voltages & uncertainties, for sensitivities and
        uncertainties and for the standard deviations. Imports the data for each one 
        from the csv files where they are stored and saves them
        Args: 
            None
        Returns:
            None
        '''

        self.nulls = np.empty(self.number)
        self.sensitivities = np.empty(self.number)
        self.nulls_uncertainties = np.empty(self.number)
        self.sensitivities_uncertainties = np.empty(self.number)
        self.stds = np.empty(self.number)

        nulls_path = Path(__file__).resolve().with_name('nulls.csv')
        nulls_and_uncertainties = pd.read_csv(nulls_path)
        self.nulls = nulls_and_uncertainties.iloc[0].to_numpy()
        self.nulls_uncertainties = nulls_and_uncertainties.iloc[1].to_numpy()

        sens_path = Path(__file__).resolve().with_name('sens.csv')
        sens_df = pd.read_csv(sens_path)
        for i in range(self.number):
            self.sensitivities[i] = np.mean(sens_df[sens_df.columns[i]].abs())

        sens_uncertainties_path = Path(__file__).resolve().with_name('uncertainties.csv')
        uncertainties_df = pd.read_csv(sens_uncertainties_path)
        for i in range(self.number):
            self.sensitivities_uncertainties[i] = np.mean((uncertainties_df[uncertainties_df.columns[i]]).abs())

        std_path = Path(__file__).resolve().with_name('stds.csv')
        std_df = pd.read_csv(std_path)
        self.stds = std_df.iloc[0]


    def into_voltage(self) -> None:
        '''
        method for converting the numeric outputs from the sensors into voltages
        the null voltages for each sensor are also subtracted from the data here. 
        Calculates the uncertainty associated with each voltage
        Args:
            None
        Returns:
            None
        ''' 

        self.data = read_data(self.port, self.filename, self.samples)

        self.voltage_uncertainty = [0] * self.number

        for i in range(self.number):
            self.sensor_uncertainty = np.sqrt(0.25 + self.stds.iloc[i])
            if i <= 7:
                average_reading = self.data[self.data.columns[i+1]].mean()

                self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] * self.vcc / self.bits

                average_voltage_1 = self.data[self.data.columns[i+1]].mean()
                readings = self.sensor_uncertainty / average_reading
                vcc = self.vcc_un / self.vcc
                rooted = np.sqrt((readings)**2 + (vcc)**2)
                v1_uncertainty = average_voltage_1 * rooted

                self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]]-self.nulls[i]

                self.voltage_uncertainty[i] = np.sqrt((self.nulls_uncertainties[i])**2 + (v1_uncertainty)**2)

    def field_strengths(self) -> None:
        '''
        method for converting the voltages into field strengths using the calculated sensitivity
        values for each sensor from the calibration steps. field strengths are calculated in mT.
        calculates the uncertainty of each field strength measurement
        Args:
            None
        Returns:
            None
        '''

        self.field_uncertainty = [0] * self.number

        for i in range(self.number):

            voltage = (self.voltage_uncertainty[i]/self.data[self.data.columns[i+1]].mean())**2

            self.data[self.data.columns[i+1]] = (self.data[self.data.columns[i+1]]/(self.sensitivities[i]/1000))*1000

            sensitivity = (self.sensitivities_uncertainties[i]/self.sensitivities.mean())**2
            self.field_uncertainty[i] = np.sqrt((sensitivity+voltage))

        new_names = ['time/s']
        new_names.extend([f'field_strength_S{i}/mT' for i in range(1, self.number + 1)])
        self.data.columns = new_names

        self.data[self.data.columns[0]] = self.data[self.data.columns[0]].astype(float)

        self.data['time/s'] = self.data['time/s']/1000

    def display_uncertainty(self) -> None:
        '''
        converts the relative uncertainties for the field strengths into absolute uncertainties and 
        displays them in the output
        Args:
            None
        Returns:
            None
        '''

        field_display = self.data.copy()

        for i in range(self.number):
            column = field_display.columns[i+1]

            relative_uncertainties = self.field_uncertainty[i]

            field_display[column] = field_display[column].apply(lambda x: f'{x:.3f} ± {abs(x*relative_uncertainties):.3f}')

        print(field_display)

    def run(self):
        '''
        method for running the methods within this class. This method is called in the 
        `__init__()` method and allows the class to be called from outside only once
        Args:
            None
        Returns:
            None
        '''

        self.get_params()
        self.into_voltage()
        self.field_strengths()
        self.display_uncertainty()
        