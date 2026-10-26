# Calibrating sensor array

At the beginning of a new experiment, or every time the array has changed, it will need to be calibrated to its new setup. The calibration should be performed in the same conditions as the experiment will be (not the magnetic fields but the physical environment). Before the calibration can begin the Arduino sketch corresponding to the sensor array setup being used needs to be uploaded to the Arduino board. This is done by opening the sketch in the Arduino IDE and press upload with the board plugged in to the computer. 

## Instructions for calibration

The first stage of the calibration is to find the null voltage of each sensor. In this step, it will also identify the associated uncertainty with these measurements and the noise floors (standard deviations) of each sensor in the array. The null voltage is the base voltage outputted when no field is present, this baseline voltage must be subtracted from the rest of the readings otherwise it will show up as a systematic error throughout. This value should be about half of the input voltage (vcc), however will need to be calculated for each sensor as it wont be exactly 2.5V (or half the vcc). Without this, the end results could be incorrect.

These properties can be calculated using the `nulls.py` script in the '1D_array' directory or the `3D_nulls.py` script in the '3D_array' directory. The number of samples these parameters are calculated over can be inputted. The rest of the inputs must be accurate to the sensor array. This measurement should be done with no fields present and in the same location as the sensors will be for the rest of the calibration and for the experiment.

Once these have been calculated, the sensitivities of each sensor can be calculated using the `sens.py` script or the `3D_sens.py` script. This will require a field input, and this part of the calibration needs to be done under a calibration field of known field strength. The field(s) can be measured using a magnetic field probe at the location of the sensor array within the field. If doing 3D calibration, the field inputs will be in an array format (e.g  calibration_field = [30, 45, 60], in the order of x field, y field, z field). The field inputs are in units of mT. 

This part of the calibration can be repeated for multiple calibration fields, each time it runs, a value of sensitivity (conversion factor between voltage and field strength) and its uncertainty is calculated and appended to a data file. After all the calibrations have been done, it will take an average value for each sensor (the sensitivity values are field independent) and use that in conversions going forward. 

You are able to remove anomalous calibrations, if the results are incorrect or something went wrong during the calibration, those entries can simply be deleted from the csv files that the sensitivities will be stored in. The `filename` parameter in the `Sensitivity` class refers to the file that the calibration data is stored in so make sure to change this along with the calibration field inputs to ensure the data is all saved and not overwritten. 

Once this is complete, the sensor array will be calibrated, the csvs generated will store both the calibration data but also the calculated calibration parameters, these will be read in by the `fields.py` or `3D_fields.py` and used for conversion. 

### tips for calibration

1. stable calibration field is required (need all sensors in array to be under the same field strength)
2. take as many samples as possible in each field (including for no fields) to get accurate results
3. do multiple calibration field strengths
4. try and calibrate in the same position as the array will be in for the experiment if possible
5. check that results are what is expected (low uncertainties, null voltages of approx. half the vcc, sensitvities of about 3.125 mV/Gauss
