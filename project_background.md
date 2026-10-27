# Project Background

## Project Motivation

talk about why this is important

## Calculations

Using Hall Effect sensors allows for easy conversion between a ratio metric output and measured field strengths. Each sensor has a conductive plate in it, called the 'Hall Element'. When placed under a magnetic field, a voltage is created across the plate and that potential difference is proportional to the field it is placed under. 

The output of the sensor will be an integer within the range of the resolution (bit depth) of the analogue to digital converter(ADC) being used. For an Arduino Nano which has a bit depth of 8, that corresponds to 1024 levels so the output will be a number between 0 and 1023. This number is converted into a voltage using the following relationship:
```math
Voltage = sensor\; count x vcc / bit\; depth
```
The VCC is the voltage at common collector (just the total range that the voltage can take). This voltage then needs to be adjusted to account for the null voltage (usually about half of the vcc) which is calculated for each sensor in the calibration steps for each sensor array.

```math
 Potential\;Difference = Voltage - V_{null} 
```
This potential difference is then directly proportional to the field strength the sensor is placed in. The proportionality factor is a property of the sensor called the 'sensitivity', this value is also calculated during the calibration of the sensor array, its typical value for the sensors used is 3.125mV/Gauss, however, like the null voltage they must be calculated during calibration for each sensor as they won't be the same for all of them. 
```math
Voltage = Sensitivity x Field\; Strength
```
This is then used on every data entry to convert them to fields. The uncertainties for each one is also calculated. This is done using the method of propagation of uncertainties. The absolute uncertainty in each sensor calculation/measurement is found as a percentage and then multiplied by the field value. This is the output of the conversion program:

<img width="763" height="356" alt="image" src="https://github.com/user-attachments/assets/252d4d3d-f821-48fc-9b9d-2c1fb796dd9b" />

## Calculating Uncertainties
The method for calculating uncertainties is using the propagation of uncertainties. For more on this method see [here](https://www.mso.anu.edu.au/pfrancis/labskills/uncertainties/Propagation_Equations.pdf)

### Uncertainties in the null voltages calculations

The equation for calculating the null voltage is:  
```math
V_{null} = sensor\; count\; x\; vcc / bit\; depth
```

Therefore, the uncertainty in the null voltage can be calculated by using the following equation:
```math
(\frac{\delta\;V_{null}}{V_{null}) = ((\frac{\delta\;count}{count})^2 + (\frac{\delta\;vcc}{vcc})^2 + (\frac{\delta\;bit\;depth}{bit\;depth})^2)^{0.5}
```
where:
```math
(\frac{\delta\;count}{count})^2 = (\delta\;sensor)^2 + (std)^2
```

These uncertainty calculations are performed in `nulls.py` and `3D_nulls.py` in the `find_uncertainties_in_null()` and `uncertainties_in_nulls()` methods for 1D arrays and 3D arrays respectively.

### Uncertainties in sensitivities calculation

```math
voltage = field\;strength\;x\;sensitivity
```
Therefore:
```math
(\frac{\delta\;sensitivity}{sensitivity})^2 = (\frac{\delta\;field}{field})^2 + (\frac{\delta\;Voltage}{Voltage})^2
```

where
```math
(\frac{\delta\;Voltage}{Voltage})^2 = (\frac{\delta\;count}{count})^2 + (\frac{\delta\;vcc}{vcc})^2 + (\frac{\delta\;bit\;depth}{bit\;depth})^2 + (\delta\;V_{null})^2
```
and 
```math
(\frac{\delta\;count}{count})^2 = (\delta\;sensor)^2 + (std)^2
```
Therefore, combining the three equations, $(\frac{\delta\;sensitivity}{sensitivity})^2$:

```math
(\frac{\delta\;sensitivity}{sensitivity})^2 = (\delta\;sensor)^2 + (std)^2 + (\frac{\delta\;vcc}{vcc})^2 + (\frac{\delta\;bit\;depth}{bit\;depth})^2 + (\delta\;V_{null})^2 + (\frac{\delta\;field}{field})^2
```

This is calculated in the `sens.py` and `3D_sens.py` scripts in the `perform_calibration()` method for both 1D and 3D arrays.

### Calculating uncertainty in field measurements

The uncertainties in the null voltages and the sensitivities are saved when they are calculated and fed back into the equations for calculating the uncertainty in the field measurement.

```math
field\;strength = voltage\;/\;sensitivity
```
so,

```math
(\frac{\delta;field\;strength}{field\;strength})^2
```
the uncertainty of the sensitivity measurement is already known, so only the voltage measurement needs to be calculated, this uses the exact same formula as before, but is redone as there will be different values for each quantity. The equation isn't written out again here as it can be seen above. These calculations are done in the `fields.py` and `3D_fields.py` scripts in the `into_voltage()`, `field_strengths()` methods in both scripts.
