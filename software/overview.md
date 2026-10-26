# Software overview

The software portion of this project comprises of an Arduino, a python code and interpolation software for field visualisations. The Arduino code is responsible for telling the Arduino what format and order it should read the data from the hall effect sensors from. The python code is for interpreting this data, calibrating the sensors and converting the incoming data into field and uncertainty measurements. The interpolation software is for visualising the field measurements.

## Arduino code

The Arduino code is fairly simple. It is important that the order in which the Arduino reads the data from the sensors is known. Each sensor is attached to an electronic address, by specifying which order these addresses are read in and knowing which sensor is attached to each address, the order of the sensors is known. The code cycles through each I2C port on the multiplexer and then within each cycle, cycles through each analogue to digital converter (ADC) attached to each multiplexer (maximum 2 - addresses of 0x48 or 0x49). In each ADC, there are 4 analogue ports which are read in succession before moving onto the next ADC. Uses the Serial library to read from the sensors.

## Python code

The python code is comprised of two parts: 1D calibration and 3D calibration. The difference between these two is just that for the 3D calibration, the x, y, z data must be processed separately as they will be subjected to different fields. For the calibration, they must be separate as they will compared against different field values. Apart from that, the two methods work similarly:
- data is read from the Arduino using the serial library
- the null voltages, standard deviations (noise) and uncertainties in null voltages are calculated when the array is under no magnetic field
- once the array is placed into a field, that value is inputted to have the array to be calibrated against 

### 1D calibration
Data is read from the Arduino and read into the python scripts. The null voltages can be calculated, then the sensitivities and then the sensor array is calibrated and the fields script can be used to measure field strengths across the array. 

#### Key Classes and Methods

##### Classes

###### Nulls class:
calculates the null voltage, associated uncertainty and the standard deviation of each sensor in a 1D array.
Attributes:
* `number (int)`: the number of sensors in the array
* `port (str)`: the computer port that the array is connected to
* `vcc (float)`: the value of the VCC of the Arduino
* `filename (str)`: the name that the data will be stored under
* `vcc_un (float)`: the associated uncertainty with the reading of the vcc of the Arduino
* `bits (int)`: the bit depth of the microcontroller
* `samples (int)`: how many samples are read to get the values for null voltage and standard deviation

Methods:
* `find_params() -> None`: eads in the data and calculates the standard deviation of each sensor as well as the null voltages
* `find_uncertainties_in_null() -> None`: calculates the uncertainty associated with each calculation for null voltage that was just done.
* `save_values() -> None`: saves null voltages, uncertainties and standard deviations in csvs so that they can be accessed for the next calibration step and for data conversion.

###### Sensitivity class:
class for calculating the sensitivity of each sensor and its uncertainty. takes input of a known field value and scales up the outputted voltage correctly. Also has a method for comparing the field created by the hemlholtz coil as measured by the magnetic field probe and what field should be produced based on the current being fed through the coil,the radius of the coils and the number of turns present in the coil. saves the values for sensitivity for each sensor to be used as scale factors in data conversion.

Attributes:
* number (int): the number of sensors present in the sensor array
* port (str): the computer port that the Arduino is connected to (which port needs to be read from)
* vcc (float): the value of the VCC (input voltage) from the Arduino/external power supply
* vcc_un (float): the associated uncertainty with the value obtained for the VCC
* filename (str): the filename where the data from the sensors is read into
* bits (int): the bit depth of the analogue-digital converter (ADC)
* samples (int): the number of samples taken and used for these calculations
* calibration_field (float): the value of the field that the sensor array is being calibrated against
* field_uncertainty (float): the uncertainty in the measurement of the field that the sensors are calibrated against

Methods:
* get_parameters() -> None: imports and saves the parameters found during calibration (null voltages and uncertainties for each sensor in the array) found so far.
* current_comparison(current: float, current_uncertainty: float, number_of_turns: int, radius_of_coils: float) -> None: calculates what the theoretical field value should be based on the current sent through the coil, the radius of the coil and the number of turns in the coil
* perform_calibration() -> None: calculates the scale factor required to get from the voltage value outputted into the value of the known calibration field with its uncertainty
* saves_sens() -> None: saves the values calculated for the sensitivity of each sensor and the uncertainty in sensitivity for each sensor in csv files so that they can be accessed later. the csv files are appended each time the class is run (for different calibration field values)

###### Conversion class:
class for converting the raw data read from the hall effect sensors and the Arduino into useful data (field strengths for each sensor and time stamps). Uses the null voltage and sensitivity values calulated during the calibration steps. Calculates the uncertainty in each field measurement

Attributes:
* port (str): the port of the computer that the arduino/hall effect sensor array is plugged in to
* filename (str): the name of the csv file that stores the data being read - is converted to a pandas dataframe for easier manipulation
* number (int): the number of sensors in the array - provides information for how many iterations are required
* vcc (float): the VCC (voltage output) of the arduino into the sensors
* vcc_un (float): the associated uncertainty with the value of the VCC
* samples (int): the number of data samples taken

Methods:
* get_params() -> None: reads the csvs file where the calibration parameters (null voltages/sensitivity/uncertainties) are stored and saves them as arrays so that they can be used in this class for the conversion
* into_voltage() -> None: multiplies the numbers outputted by the sensors to convert them into voltages,and subtracts the null voltage for each sensor off of that sensors readings. Calculates the uncertainty in the voltage at this stage for each sensor
* field_strengths() -> pd.DataFrame: converts the voltages into field strengths by dividing by the sensitivity and calculates the associated uncertainty with each field measurement. renames the data frame headings
* display_uncertainty() -> None: uses the calculated fractional uncertainty and applies it to each value of the field, displays them in the output data frame
* run() -> None: method for running the other methods in the class

##### Methods
1. `read_data(port:str, filename: str, samples: int=200) -> pd.DataFrame`: uses the serial library to get data from the Arduino and saves it as a csv file.
Args:
- port (str): computer port that the Arduino is connected to
- filename (str): filename that the data is saved under (csv)
- samples (int): how many samples (timestamps) are read
Returns:
- df (pd.DataFrame): the data frame that the Arduino data is stored in
### 3D Calibration

#### Key Classes and Methods
##### Classes
Nulls Class:
- 

Calibrate Class:
- 

Convert Class:
- 

##### Methods
- read_data()
- split_data()
