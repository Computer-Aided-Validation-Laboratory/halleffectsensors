# Project Background

## Project Motivation

talk about why this is important

## Calculations

Using Hall Effect sensors allows for easy conversion between a ratio metric output and measured field strengths. Each sensor has a conductive plate in it, called the 'Hall Element'. When placed under a magnetic field, a voltage is created across the plate and that potential difference is proportional to the field it is placed under. 

The output of the sensor will be an integer within the range of the resolution (bit depth) of the analogue to digital converter(ADC) being used. For an Arduino Nano which has a bit depth of 8, that corresponds to 1024 levels so the output will be a number between 0 and 1023. This number is converted into a voltage using the following relationship:

**Voltage = sensor count x vcc / bit depth**

The VCC is the voltage at common collector (just the total range that the voltage can take). This voltage then needs to be adjusted to account for the null voltage (usually about half of the vcc) which is calculated for each sensor in the calibration steps for each sensor array.

$\ Potential Difference = Voltage - Null Voltage $

This potential difference is then directly proportional to the field strength the sensor is placed in. The proportionality factor is a property of the sensor called the 'sensitivity', this value is also calculated during the calibration of the sensor array, its typical value for the sensors used is 3.125mV/Gauss, however, like the null voltage they must be calculated during calibration for each sensor as they won't be the same for all of them. 

**Voltage = Sensitivity x Field Strength**

This is then used on every data entry to convert them to fields. The uncertainties for each one is also calculated. This is done using the method of propagation of uncertainties. The absolute uncertainty in each sensor calculation/measurement is found as a percentage and then multiplied by the field value. This is the output of the conversion program:

<img width="763" height="356" alt="image" src="https://github.com/user-attachments/assets/252d4d3d-f821-48fc-9b9d-2c1fb796dd9b" />

## Calculating Uncertainties
The method for calculating uncertainties is using the propagation of uncertainties. For more on this method see [here](https://www.mso.anu.edu.au/pfrancis/labskills/uncertainties/Propagation_Equations.pdf)

### Uncertainties in the null voltages calculations

The equation for calculating the null voltage is:    
**null voltage = sensor count x vcc / bit depth **

Therefore, the uncertainty in the null voltage can be calculated by using the following equation:



