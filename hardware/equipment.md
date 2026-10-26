# Equipment List

## Initial component order

To start with, will make a smaller experimental setup to ensure that the circuit is correct and the software works with it. The components being used for this are as follows:

### Hall effect sensors
* ordered 10 analog hall effect sensors to start with
* the sensors being used for this project are SS495A sensors
* they are ratiometric sensors so output a value between 0 and 1023 rather than directly outputted a voltage. This value is proportional to the voltage outputted and is scaled by the the VCC/1023
* the VCC is 5 V for these sensors
* they measure magnetic field strength/voltages in only one direction at a time
* [data sheet](https://4donline.ihs.com/images/VipMasterIC/IC/HWSC/HWSC-S-A0015601488/HWSC-S-A0015601488-1.pdf?hkey=CECEF36DEECDED6468708AAF2E19C0C6)

### Capacitors
* the [capacitors](https://docs.rs-online.com/85f8/A700000007244452.pdf) ordered are 100nF capacitors and they will help with noise reduction of the signal
* these are placed in parallel with the sensors, geographically as close as possible to them
* these might prove obsolete when the DAQ gets involved as that should also help with noise reduction

### Arduino
* using an [Arduino nano](https://docs.arduino.cc/resources/datasheets/A000005-datasheet.pdf) for this project - is very small so should work well
* has a 5 VDC output which is perfect for the SS495A sensors being used
* has 8 analog output pins so when scaling up the project will need multiplexers

### DAQ
* the DAQ being used is the spec of [NI-9219](https://www.ni.com/en/shop/hardware/strain--pressure--and-force/model-ni-9219?srsltid=AfmBOorT6p0ZeMICqpSZI00pWWvoCxniAMpPfJt9fDPkkUH79xjW8_fR)
* will be used to take the data from the arduino and into the computer.

### Others
* Breadboard - ordered two small [breadboards](https://docs.rs-online.com/509f/A700000007388301.pdf), to start with will be using this - gives structure to the array and is handy for testing and constructing circuits
* Jumper wires - ordered a variety of types for whatever i might need them for (30 x male to male, 10 x female to male and 10 x female to female)
* USB cable - will be used to connect the arduino nano to laptop

Everything above was ordered for the initial setup, the circuit is being improved to accommodate many more sensors into the array, the equipment above will all be used in the new setup as well, with the addition of everything below. 

--------------------------------------------------------------------------------------------------------------------------------------

## New component order 

### Wires
* 30 x male to female breadboard jumper [wires](https://docs.rs-online.com/285e/0900766b812bf0ed.pdf)
* 40 x female to female breadboard jumper [wires](https://docs.rs-online.com/db94/0900766b812bf0ee.pdf)
* 60 x male to male breadboard jumper [wires](https://docs.rs-online.com/b685/0900766b812bf0f0.pdf)
* 5 x grove [cables](https://docs.rs-online.com/5ba8/A700000006828213.pdf)
* 10 x grove to male jumper [cables](https://docs.rs-online.com/68c4/A700000006828209.pdf)
* 10 x grove to female jumper [cables](https://docs.rs-online.com/a5d7/A700000006828221.pdf)

### Sensors/capacitors
* 20 x SS495A Hall Effect [Sensors](https://4donline.ihs.com/images/VipMasterIC/IC/HWSC/HWSC-S-A0015601488/HWSC-S-A0015601488-1.pdf?hkey=CECEF36DEECDED6468708AAF2E19C0C6)
* 20 x 0.1 microF [Capacitors](https://docs.rs-online.com/85f8/A700000007244452.pdf)

### Others
* 1 x extra [breadboard](https://docs.rs-online.com/509f/A700000007388301.pdf) for wire channels
* 6 x ADS1115 ADC [module](https://docs.rs-online.com/38a8/A700000007466213.pdf)
* 1 x grove [shield](https://www.farnell.com/datasheets/3761223.pdf?_gl=1*1vpxd86*_gcl_aw*R0NMLjE3OTMwMjc1MzkuRUFJYUlRb2JDaE1JMmRmRmlmelhsd01WT1pGUUJoMnFfRHRfRUFBWUFTQUFFZ0pNYV9EX0J3RQ..*_gcl_au*NTU0NTc2NjAyLjE3ODgzNTcxNzcuLS4tLjE3OTAzMjgwNDcuNDAyODQxMTU3LjE3OTMwMjc1MzguMTc5MzAyNzc1MA..) for Arduino nano
* 1 x 8-port I2C hub [multiplexer](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/57/103020293_Web.pdf)



