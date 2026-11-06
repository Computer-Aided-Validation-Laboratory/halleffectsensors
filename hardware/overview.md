# Experimental Design

The Hall Effect Sensor array is going to be used as a magnetic camera during DIC experiments. This allows for live monitoring of constant or variable magnetic fields. The set-up must be designed in such a way that the DIC still has total visual access to the test sample, but the magnetic field measurements are still accurate. 

The hardware used to hold the array in place and know where the measurements are being taken from is being designed on CAD software and will be 3D-printed. 

The circuit for a larger sensor array has been designed and will be tested. The end goal with this design is to be in the form of printed circuit boards (PCBs). they can be customised to the DIC setup and have the shape of the sample. Different strength sensors can be used for different experiments to give the most accurate answers.

The sensors being used currently for development and testing are 1 dimensional, analogue Hall Effect sensors. To get 3D field measurements over the test samples, three times as many sensors will need to be used (1 for each direction), they can be incorporated into the PCB design.

The biggest challenge of this project is the experimental design of the array due to the limitations that come with DIC experiments and not being able to compromise that setup.

The intermediate step between using a breadboard and a PCB will be to design something that can hold a 3D array of sensors but still requires some soldering. A prototype of this has been designed on CAD: 
<img width="2216" height="413" alt="image" src="https://github.com/user-attachments/assets/5308dae6-a96a-4c0c-a17f-17f59bf6c440" />

Obviously this is a very basic design that will just allow 24 sensors to slot into it, 3 in each direction, but the wires these are connected to can be soldered to the underside of these sensors and the capacitors can be soldered across the pins of the sensors. For the sensors facing parallel to the surface of this support structure (probably the ones in the top slot of the sensor holes parallel to the long sides of the structure) they will simply be bent backwards (this does not affect the sensor readings as was seen in the third calibration trial of a sensor array where this was tested) to be facing the correct way. This should work with the new setup and 6 ADCs, once this design has been successfully tested, the PCB of this circuit can then be designed and tested. 
