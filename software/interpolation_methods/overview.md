# Interpolation Methods

The end goal for the visualisation of the fields is to be able to view this in MatchID. The current setup is just python mapping of the fields as a way to visualise the fields before the MatchID link is made. The code runs from `example_plot.py` and takes inputs for the data being mapped, the setup of the sensor array and the filename for where the animation is stored. 

The output is an mp4 file, which will be saved in this directory and also displayed when the file is run. For this software it is imperative that the information in the json is correct and the coordinates are corresponding to their physical position.

The script gets the raw count data from the csv file and converts it to field measurements to display. There is an input for what direction of the field to be mapped. 

The output looks like a map like this (obviously in video form):
<img width="463" height="547" alt="image" src="https://github.com/user-attachments/assets/32141446-ef54-410a-b68a-459b6ffbae31" />
