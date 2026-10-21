---------------------------------------------------------------------------------------------------------------
# Software Overview - super out of date!!!

The software in this project is responsible for taking the data collected by the hall effect sensors and converting it into useful magnetic field strength data. It comprises of arduino software for data collection and python software for converting the raw data into useful data. 

----------------------------------------------------------------------------------------------------------------
## Structure of software directory
```
software/
|---- README.md
|---- src/
|     |---- arduino_code/
|           |---- arduino_code.ino   # code for data collection
|     |---- python_code/
|           |---- calibration_script.py    # script to run for calibrating sensors
|           |---- calibration.py       # does the calibration calculations, determines the sensitivities and null voltages of the sensors
|           |---- conversion.py         # converts the data from ratiometric outputs to field strengths, uses null voltages and sensitivities found in calibrate.py and calib_script.py       
|           |---- conversion_script.py  # where the conversion is run from
|           |---- read.py            # contains method for reading in data from arduino into csv, imported and used in many files
```
----------------------------------------------------------------------------------------------------------------
## Arduino code
This is pretty simple software. Uses the serial monitor to print a time stamp and also the sensor reading for however many sensors is being used. Very customisable and scalable for any number of sensors, will simply create a new column in the code. This code below is for 2 sensors, however can be used for any number of sensors up to and including 8 sensors (as that is how many analogue pins the Arduino has)
<img width="1076" height="706" alt="image" src="https://github.com/user-attachments/assets/8791c006-0acb-45ad-8cb5-29af59010a5b" />

----------------------------------------------------------------------------------------------------------------
## Python code
libraries used: pandas, numpy, matplotlib, serial, csv, pathlib, time   
The python code is where most of the data processing will occur, when it recieves the data from the arduino, it reads it and saves it as a csv. This is then converted into a pandas dataframe for easier use. 

When the data arrives it is a table that will look something like this:
```
.......................................
 time        sensor1           sensor2
 0            2041               1983
 500          2037               1976
 1000         2031               1982
 1500         2039               1981
.......................................
```
The code is structured so that there are two scripts designated to both the sensor calibration and the data conversion. The fifth script is just for reading the data from the Arduino and is called upon and used in both `conversion.py` and `calibrate.py`. 

The null voltages and sensitivities will only need to be found once, at the beginning, during the calibration steps, however the null voltages must be found first and used to calculate the sensitivities. Both these properties need to be used and included in calculations for every data conversion process forward. They are saved first as a data frame and then saved together in a csv file which is read in for data collection.

---------------------------------------------------------------------------------------------------------------
### Key classes and methods:
#### Classes: 
scripts contains a class for sensor calibration and data conversion
- `Calibrate`: Class for calibrating the sensors, calculates the calibration parameters of the null voltage and the sensitivity of each sensor   
  - Attributes:    
        - `number (int)`: number of sensors present in the array    
        - `port (str)`: name of the computer port the arduino is linked to   
        - `vcc (float)`: value of the VCC output from the arduino    
        - `filename (str)`: csv filename the data is stored in      
        - `samples (int)`: how many data samples each reading takes   
        - `delay (int)`: the time between calibration recordings    
  - Methods:    
        - `find_null_voltage() -> pd.DataFrame`: computes and stores null voltages for each sensor in the array   
        - `perform_calibration() -> pd.DataFrame`: computes and stores the average value for sensitivity for each    sensor     
       
- `Convert`: class for converting the raw data read from the hall effect sensors and the Arduino into useful data (field strengths for each sensor and time stamps). Uses the null voltage and sensitivity values calulated during the calibration steps.    
   - Attributes:    
       - `port (str)`: the port of the computer that the arduino/hall effect sensor array is plugged in to   
       - `filename (str)`: the name of the csv file that stores the data being read - is converted to a pandas dataframe for easier manipulation    
       - `number (int)`: the number of sensors in the array - provides information for how many iterations are required     
       - `vcc (float)`: the VCC (voltage output) of the arduino into the sensors samples (int): the number of data samples taken      
   - Methods:
       - `get_params() -> None`: reads the csv file where the calibration parameters are stored and saves them as arrays so that they can be used in this class for the conversion     
       - `into_voltage() -> None`: multiplies the numbers outputted by the sensors to convert them into voltages and subtracts the null voltage for each sensor off of that sensors readings    
       - `field_strengths() -> pd.DataFrame`: converts the voltages into field strengths by dividing by the sensitivity    
       - `run() -> None:` method for running the other methods in the class    

#### Methods:   
The only method present that doesn't come under another class:     
- `read_data(port: str, filename: str)`: this method is used in many scripts, this is how the scripts get the data from the arduino. This takes inputs of what port the arduino is connected to and what name the data should be saved under. It reads it in using the serial library and writes it to a csv file before converting it in a pandas dataframe for data processing. only method found in `read.py`

Basically, the calibration runs and determines the null voltage and the sensitivity of each sensor in the array, this is then stored in a csv file called 'combined-data.csv', this csv file is then read in to the conversion code and the values are extracted to be used again. The conversion code then converts the sensor outputs to magnetic fields. The output of the conversion code looks like this: 

<img width="1741" height="381" alt="image" src="https://github.com/user-attachments/assets/02bd930f-f168-415a-b204-157c3baae269" />

(The values for the magnetic fields are incorrect as this was not calibrated in real fields.) 
