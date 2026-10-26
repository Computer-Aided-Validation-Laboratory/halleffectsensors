# Hall Effect Sensor Array

This repo contains all information about the hall effect sensor array. The aim of this project is to create a 'magnetic field camera' made up of hall effect sensors. This repo contains information on constructing the array, calibrating the array and using it to measure live magnetic fields.

This 'camera' is being designed for use in DIC experiments to visualise the magnetic fields over different areas of a test sample whilst it is undergoing deformation.

This repo contains a hardware directory including things like circuit design, equipment lists, component designs, PCB plans and an overview of all the hardware (experimental side of the project). **paste link here**

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
|---- overview.md                         # overview of software directory (linked above)
|---- src/
|     |---- arduino_code/                 # for data reading
|           |---- extended_code/
|                 |---- extended_code.ino # Arduino code for larger array (uses ADS115 library)
|           |---- initial_code/
|                 |---- initial_code.ino  # Arduino code for initial setup (less than 9 sensors)
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
