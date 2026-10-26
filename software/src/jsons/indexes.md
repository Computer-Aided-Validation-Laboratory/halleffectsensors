# Indexing the sensors in the array

The Arduino cycles through each electronic address in order. It is known what order the electronic addresses are read in as it is specified in the Arduino code, however the software must know which direction the sensor is pointing at this address and what the physical location of it is. The indexing allows us to relate what column of the incoming data corresponds to what direction the sensor is facing and its coordinate. The electronic address and the index of the sensor are the same property, the index is just easier to use to sort the data.

The Arduino reads the data from each I2C port first, then within that port it will read each analogue to digital converter attached (maximum of two) and then on each one of those it reads the analogue ports A0 - A3.

The order of indexing is specified below. This ordering is for the maximum number of sensors used (64), however if not all of these sensors are being used, just index the sensors in the order of electronic addresses below. E.g if you only have sensors connected to electronic addresses corresponding to below indexes of: 1, 2, 5, 18, 19, 20, do not give these as those numbers, give them as indexes 1, 2, 3, 4, 5. 

The electronic addresses will have three parts; 1. the I2C hub channel, 2. the address of the ADC within the I2C port and 3. the analogue port it is connected to on the ADC (A0 - A3)

## Ordering of indexes:
| Index | Electronic Address |
| ---- | ---- |
| 1 | I2C0, 0x48, A0 |
| 2 | I2C0, 0x48, A1 |
| 3 | I2C0, 0x48, A2 |
| 4 | I2C0, 0x48, A3 |
| 5 | I2C0, 0x49, A0 |
| 6 | I2C0, 0x49, A1 |
| 7 | I2C0, 0x49, A2 |
| 8 | I2C0, 0x49, A3 |
| ..|................|

