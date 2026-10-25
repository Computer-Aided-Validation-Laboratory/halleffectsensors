------------------------------------------------------------------------------------------------------------------------
# Software overview

The software portion of this project comprises of an Arduino, a python code and interpolation software for field visualisations. The Arduino code is responsible for telling the Arduino what format and order it should read the data from the hall effect sensors from. The python code is for interpreting this data, calibrating the sensors and converting the incoming data into field and uncertainty measurements. The interpolation software is for visualising the field measurements.

------------------------------------------------------------------------------------------------------------------------
## Arduino code

The Arduino code is fairly simple. It is important that the order in which the Arduino reads the data from the sensors is known. Each sensor is attached to an electronic address, by specifying which order these addresses are read in and knowing which sensor is attached to each address, the order of the sensors is known. The code cycles through each I2C port on the multiplexer and then within each cycle, cycles through each analogue to digital converter (ADC) attached to each multiplexer (maximum 2 - addresses of 0x48 or 0x49). In each ADC, there are 4 analogue ports which are read in succession before moving onto the next ADC. Uses the Serial library to read from the sensors.

-------------------------------------------------------------------------------------------------------------------------
## Python code

The python code is comprised of two parts: 1D calibration and 3D calibration. The difference between these two is just that for the 3D calibration, the x, y, z data must be processed separately as they will be subjected to different fields. For the calibration, they must be separate as they will compared against different field values. Apart from that, the two methods work similarly:
- data is read from the Arduino using the serial library
- the null voltages, standard deviations (noise) and uncertainties in null voltages are calculated when the array is under no magnetic field
- once the array is placed into a field, that value is inputted to have the array to be calibrated against 

### 1D calibration
Data is read from 
#### Key Classes and Methods
