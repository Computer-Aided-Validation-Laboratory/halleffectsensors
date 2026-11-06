# Interpolation Methods

The field will eventually be visualised using a live feed from a National Instruments (NI) Data Aquisition (DAQ) system feeding into MatchID. In the mean time the fields used for calibration and otherwise are being visualised in python using the `griddata()` function to interpolate the points. This not currently an exact method however just works to check the software is interpreting the sensor data and the coordinates of the sensors from the jsons correctly. 

The code for this is found in `plot.py` and it will produce an .mp4 file showing the field distribution across the sensor array. 
<img width="707" height="473" alt="image" src="https://github.com/user-attachments/assets/95491f5a-513f-4fc3-a13c-6fadd2f04d16" />
