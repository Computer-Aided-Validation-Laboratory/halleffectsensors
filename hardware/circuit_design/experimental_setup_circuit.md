# Experimental set-up
-------------------------------------------------------------------------------------------------------------------------------------
## How the circuit is going to work

### Equipment list:
1. Arduino Nano   
2. Grove shield for Arduino Nano   
3. 8 port I2C hub (TCa9548A) multiplexer   
4. ADS1115 ADC (x 6)   
5. Many types of wires   
6. 0.1 microF capacitors   
7. SS495A Hall Effect sensors   

--------------------------------------------------------------------------------------------------------------------------------------

### Explanation of setup

There is a central Arduino that reads all the data from all the sensors and sends it into software to be interpreted. The sensors all output a number between 0 and 65,536 (as the ADC is 16-bit), which is then processed and converted into a magnetic field of strength by the software.  

<img align="left" width="320" height="292" alt="image" src="https://github.com/user-attachments/assets/729b4440-ac5a-4885-b95f-2f3c29cfa68e" />

The Arduino is plugged into a grove shield for an Arduino (). This shield has 3 Analogue ports still: A0, A2 and A6 which correspond to the A0, A1, A2, A3, A6 and A7 pins on the Arduino Nano. There is also an I2C port which corresponds to the A4 and A5 Arduino analogue pins. A total of 6 sensors can be connected to the 3 analogue ports on the sensor, and the I2C port is used to connect to a multiplexer that will allow for more inputs. This grove shield requires no soldering to connect to the Arduino, so is handy.  

The I2C connection goes to an 8-port I2C hub which acts as a multiplexer. The one being used is the TCA9548A ().   

<img align="right" width="536" height="161" alt="image" src="https://github.com/user-attachments/assets/19f952fc-df30-49cb-9bfe-d19c6c5a2e6a" />

These are connected with a double-end Grove Cable. Each of these I2C ports can connect to two or four analogues to digital converters (ADC) depending on what the addressing of the ADC allows. The multiplexer being used only allows for two addresses in each I2C port, so this will allow 64 sensors maximum to be connected if all 16 ADCs are used.   

To start with, only 6 ADCs are being used to give 24 sensors being used on the I2C hub and 6 being available from the original unused Arduino pins giving a total of 30 sensors for 6 ADCs.   

<img align="left" width="310" height="312" alt="image" src="https://github.com/user-attachments/assets/b9f35e99-4fa8-4fd3-9674-f2f6242634a4" />

The 6 ADCs that will be used to start with can all go in different I2C ports, but when there are more than 8 ADCs, the ADDR of each ADC will need to be changed from the default 0x48 to 0x49 so that the Arduino can keep track of all the sensors. The ADCs chosen are on the left and are specifically ADS1115 ADCs which have a 16-bit output which is why the sensors will output values over such a large range (0-65,536). Connecting these two the I2C hub is slightly harder, There are two options for connecting them: 1) the ADC comes with a 4-pin pin header which can slot into the D (SDA), C (SCL), - (GND), and the + (VCC) holes, this can then be connected using a grove cable end into the I2C hub and female Dupont jumper wires onto the pins on the pin header. 2) the other option is that the ADC also comes with a cable that is a gravity cable to female Dupont jumper wires. The gravity end of the cable plugs into the white box (gravity) on the ADC, and the female ends can be connected to the I2C hub via another cable, a grove to male Dupont cable. The grove end of this cable goes into the I2C hub whilst the gravity end of the other cable goes into the ADC, and they will meet in the middle using the female and male Dupont ends.    

-------------------------------------------------------------------------------------------------------------------------------------

#### Connecting the sensors to the ADCs 

Each sensor requires a capacitor physically as close as possible, and 3 wires so will be a wiring nightmare if the wires aren’t managed correctly. The wires attaching to the sensors will need to be soldiered on as the sensors won’t be sat on a breadboard and the capacitor need to be soldiered directly across the pins.   

On the ADC, there are pins for each analogue input that can be connected to via female Dupont wires. The idea currently is that all these pins will be connected to a breadboard using female to male jumper wires and then the sensors can be connected to the breadboard from there. Multiple ADCs can connect to the same breadboard as it is just an intermediate for connecting the sensors.  

Then to get the pins of each sensor wired up to the breadboard will be using male ended Dupont wires into the breadboard and strip the ends of the wires so that they can be soldiered onto the pins.    

For the VCC and the GND connections, will use ribboned wires to keep them together, so will have 4 female ended wires going onto the ADC and then will use the breadboard negative and positive terminals to be like power buses for VCC and GND and all the sensor wires will attach from there.  

For the sensors that will be connected via the remaining 6 analogue ports on the Arduino (A0, A1, A2, A3, A6 and A7), they will be connected via a grove to male Dupont cable which will go into a breadboard. The same soldering process will happen again for these sensors as for the other ones. The grove to male Dupont cables can go into the same breadboard as the other sensors are connected to as well.  

-------------------------------------------------------------------------------------------------------------------------------------

#### Things to look out for: 

* Wire management – will get out of hand very quickly (30 sensors is at least 90 wires into the breadboard which is crazy so will need to keep them as separate as possible.  

* Will have 3 sensors in each ‘coordinate’ facing x,y,z directions to read the field that way so with 30 sensors, will only have 10 points of reading in each direction 

* When soldering, don’t apply the heat directly to the pins on the sensors as they will break, need to apply some soldier to them first and then like soldier onto the soldier (I think it's like recommended no more than 3s long contact with the pins at a time) 

* For many sensors (24 might be okay but any more than that is an issue) will need to use an external power source aside from the Arduino.  

-------------------------------------------------------------------------------------------------------------------------------------

#### For the actual sensor array setup: 

The transmission of the field data from the sensors will be done at the same time as the DIC (will do live field measurements), this means that the directional sensors all need to be present at the same time, so this reduces the overall size of the array as only one in three sensors are actually contributing to each field.  

Will design the setup for the Mini-Mera magnets first and try to get this strange ‘shelf’ thing to work with the three dimensional sensors coming out of it.    

The capacitors will be soldiered onto the pins on the hall effect sensor and fed through the holes so the sensor can sit on the shelf.   

-------------------------------------------------------------------------------------------------------------------------------------
### New Circuit Schematic
<img width="1305" height="912" alt="image" src="https://github.com/user-attachments/assets/32f719be-464a-477a-a71a-fc8542608ea8" />

