# Hall Effect Sensor Array

This repo contains all information about the hall effect sensor array. The aim of this project is to create a 'magnetic field camera' made up of hall effect sensors. This repo contains information on constructing the array, calibrating the array and using it to measure live magnetic fields.

The sensors use the hall effect to quantify magnetic fields. They output an integer that is proportional to a voltage produced across the hall element in the sensor. This voltage is proportional to the field that it is in. The voltage is calculated by converting the raw output: **Voltage = sensor count * vcc (total voltage range) / resolution**, and then the fields are found from: **Voltage = sensitivity * field strength**, where the sensitivity is found during the calibration steps. 

This 'camera' is being designed for use in DIC experiments to visualise the magnetic fields over different areas of a test sample whilst it is undergoing deformation.

This repo contains a hardware directory including things like [circuit design](https://github.com/Computer-Aided-Validation-Laboratory/halleffectsensors/blob/mapping/hardware/circuit_design/experimental_setup_circuit.md), [equipment lists](https://github.com/Computer-Aided-Validation-Laboratory/halleffectsensors/blob/mapping/hardware/equipment.md), component designs, PCB plans, [calibration instructions](https://github.com/Computer-Aided-Validation-Laboratory/halleffectsensors/blob/mapping/hardware/calibrations.md) and an overview of all the hardware (experimental side of the project). [hardware overview](https://github.com/Computer-Aided-Validation-Laboratory/halleffectsensors/blob/mapping/hardware/overview.md)

There is also the software directory which contains all of the source code for the project (includes Arduino code and python code for calibration and data processing) and an interpolation methods directory. There is a detailed markdown file in this directory that outlines exactly how the software works: [software overview](https://github.com/Computer-Aided-Validation-Laboratory/halleffectsensors/blob/mapping/software/overview.md)

## Structure of repository
```
README.md (this file)
LICENSE
.gitignore
hardware/
software/
```
### Structure of `software/`
```
software/
|---- overview.md                        # overview of software directory (linked above)
|---- uncertainty_quantification.md      # details uncertainty calculations through the code
|---- src/
|     |---- arduino_code/                 # for data reading
|           |---- extended_code/
|                 |---- extended_code.ino # Arduino code for larger array (uses ADS115 library)
|           |---- initial_code/
|                 |---- initial_code.ino  # Arduino code for initial setup (less than 9 sensors)
|     |---- jsons/
|           |---- json_formatting.md      # details instructions for making custom jsons
|           |---- indexes.md              # identifies which index corresponds to which electronic address
|     |---- python_code/                  # for data processing/interpretation
|           |---- 1D_array/
|                 |---- fields.py         # does the data conversion
|                 |---- nulls.py          # calculates the nulls
|                 |---- read.py           # reads in the data from sensor
|                 |---- sens.py           # calculates the sensitivity
|           |---- 3D_array/
|                 |---- 3D_fields.py      # does data conversion for 3D array
|                 |---- 3D_nulls.py       # calculates the nulls for 3D array
|                 |---- 3D_sens.py        # calculates the sensitivities for 3D array
|                 |---- func.py           # reads data from Arduino and splits based on direction
|---- interpolation_methods/              # for data visualisation

```
### Structure of `hardware/`
```
hardware/
|---- calibration_tests.md           # log of results from calibration tests
|---- equipment.md                   # all the equipment ordered for setup
|---- overview.md                    # overview of whole process (linked above)
|---- circuit_design/
|     |---- PCB_designs.md           # designs for PCB 
|     |---- experimental_setup.md    # details circuit setup (wiring and components)
|     |---- initial_circuit.md       # initial circuit plan
|---- component_design/
|     |---- CAD_designs.md           # designs for PCB holder/sensor support structure
```

## Instructions for use:
clone the repository and install:
```
git clone <repository-url>
cd software
pip install .
```
**need to actually make this a package (not done yet)**

Every time the array is used in a new setup, it must be calibrated. When the array is calibrated, it can be placed in an unknown field and it will produce measurements for that fields in 1 or 3 directions. For more information about calibration procedure or previous calibration results, see this document: [calibrations](https://github.com/Computer-Aided-Validation-Laboratory/halleffectsensors/blob/mapping/hardware/calibrations.md)

The idea of this project is that it can be used for any sample in any field setup, however in order for the calibration and visualisation methods to work, they must know the details about the setup being used. For using 3D calibration on an extended array (more than 8 sensors), a .json file must be used to specify the required information about each sensor in the array. This information is:     
- `"index"` : this will be an integer (not in " "), corresponding to the electronic address of the sensor (this information will be on the PCB). This document: [indexes](https://github.com/Computer-Aided-Validation-Laboratory/halleffectsensors/blob/mapping/software/src/jsons/indexes.md) details the corresponding index for each electronic address as well.   
- `"coordinate"` : For each PCB board, the 'coordinate' of each sensor will link to an index/electronic address. The software needs to know these so that it knows where (physically) the sensor is, so it knows where the field measurements are coming from in order to visualise the field. These will be in the format [x,y] (no " " and need square brackets)   
- `"direction"` : this entry will simply be "x", "y" or "z" depending on what component of the field that sensor is using. This can be determined if unsure by using the axis/direction on the calibration magnetic field probe. The sensors read fields coming towards the flat face of the sensor.

If the .json for the setup being used already exists, it can be used as normal. The parameter `json (str)` needs to be the name of the .json file detailing the information about the sensor array. E.g if the .json is called 'square.json', in every python script/class/method with an input for `json (str)`, the input parameter must be `square.json`.

For the **formatting** of the .json file, it must be done in a particular way for the code to recognise it the way it is designed to. For information about how to format it/examples, see this document: [json formatting](https://github.com/Computer-Aided-Validation-Laboratory/halleffectsensors/blob/mapping/software/src/jsons/json_formatting.md)

For information about how the uncertainties in the measurements of the fields are calculated, see this document: [uncertainties](https://github.com/Computer-Aided-Validation-Laboratory/halleffectsensors/blob/mapping/software/uncertainties.md)
