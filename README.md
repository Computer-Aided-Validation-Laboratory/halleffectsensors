# Hall Effect Sensor Array

This repo contains all information about the hall effect sensor array. The aim of this project is to create a 'magnetic field camera' made up of hall effect sensors. This repo contains information on constructing the array, calibrating the array and using it to measure live magnetic fields.

This 'camera' is being designed for use in DIC experiments to visualise the magnetic fields over different areas of a test sample whilst it is undergoing deformation.

This repo contains a hardware directory including things like circuit design, equipment lists, component designs, PCB plans and an overview of all the hardware (experimental side of the project). **paste link here**

There is also the software directory which contains all of the source code for the project (includes Arduino code and python code for calibration and data processing) and an interpolation methods directory. There is a detailed markdown file in this directory that outlines exactly how the software works: **paste link here**

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
|---- src/
|     |---- arduino_code/
|     |---- python_code/
|---- interpolation_methods/

```
going to leave this for now because it will end up changing a bunch and i don't want to waste time on it.
