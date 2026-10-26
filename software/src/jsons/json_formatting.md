# Formatting the .json file

There will be a set of standard .json files which will match to a PCB board. If you want to use a PCB board but for example with less sensors/select sensors or only in certain directions, you will need to edit the json/make a new one. I would reccomend not changing the standard .json files, but making a copy and editing as you may need it to compare to. 

The .json files are formatted in a certain way so that the python code interprets them correctly. All the sensors must be placed in "sensors" category. There is an example of the formatting below for a 3 sensor array:

<img width="527" height="486" alt="image" src="https://github.com/user-attachments/assets/4be43a62-e15a-4ee7-89ec-279b939666b4" />

All inputted sensors must be in the "sensors" square brackets. There can be as many sensors as are in the array. For more examples see the .json files in this directory.
