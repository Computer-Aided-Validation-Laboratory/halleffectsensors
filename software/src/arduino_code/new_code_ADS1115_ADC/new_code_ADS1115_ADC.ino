#include <Wire.h>   // built in arduino library (handles I2C communication protocol)
#include <Adafruit_ADS1X15.h>    // for the ADC

#define TCA_ADDR 0x70       // Default I2C address of TCA9548A (anywhere the compiler sees TCA_ADDR, it substitutes 0x70)
#define ADS_ADDR 0x48       // Default address for ADS1115 (ADDR tied to GND), as we are using a multplexer to separate them into isolated sub-buses,
// all the ADS1115 chips can share the same address

// We create one instance of the library object. 
// Since we only talk to one ADC at a time via the MUX, we can re-use it.
Adafruit_ADS1115 ads;   // creates a software object named ads based on the Adafruit library, this basically a virtual remote control
// (as the MUX only connects the nano one ADC chip at a time, only need this single object to control whichever ADC is currently active)

// Function to switch channels on the TCA9548A Multiplexer
void tcaSelect(uint8_t channel) {   //  defines function that takes an 8-bit integer (channel number) and returns no data (void)
  if (channel > 7) return; // just to check, the MUX only has channels 0 to 7, if a higher number is passed, the function stops
  
  Wire.beginTransmission(TCA_ADDR);    // opens up a communication line from the nano to the main multiplexer
  Wire.write(1 << channel); // Bit-shift to open the matching sub-bus (e.g 00000001 is channel 0, 00000010 is channel 1 and so on)
  Wire.endTransmission();    // sends the data bte and closes the trandmission, the MUX has now switched its physical internal connections
}

void setup() {   // main setup - will repeat once
  Serial.begin(9600);   // setting up the baud rate
  Wire.begin(); // Initialize I2C main bus - starts up the physical hardware inside the Arduino Nano that handles I2C communication

  Serial.println("Initializing ADS1115 units via TCA9548A...");

  // Initialize the first ADS1115 on MUX Channel 0
  tcaSelect(0);
  if (!ads.begin(ADS_ADDR)) { // attempts to start communication with the chip at 0x48
    // if it can't it will print the statement
    Serial.println("Failed to find ADS1115 on MUX Channel 0!");
    while (1); // if it can't find the ADC, this locks the Arduino in an infinite loop
    // freezing the code here so it doesn't try to read non-existenet sensors
  }
  // Optional: Adjust gain depending on sensor voltage output (Default is +/- 6.144V)
  ads.setGain(GAIN_TWOTHIRDS); // sets the voltage measurement range, configures the ADC to read voltages up to 6.144V 

  // Initialize the second ADS1115 on MUX Channel 1 - exactly the same as above
  tcaSelect(1);
  if (!ads.begin(ADS_ADDR)) {
    Serial.println("Failed to find ADS1115 on MUX Channel 1!");
    while (1);
  }
  ads.setGain(GAIN_TWOTHIRDS);

  Serial.println("System Ready!");
}

void loop() {
  // Loop through 2 Multiplexer channels (Change to 8 if utilizing all MUX slots)
  for (uint8_t m_chan = 0; m_chan < 2; m_chan++) { // loop that runs twice per cycle. creates temporary variable m_chan. It starts
    // at 0, runs the code inside, increments by 1 (m_chan++), runs the code for 1, then stops because it must stay less than 2
    // this targets our two MUX channels sequentially
    
    // 1. Tell the TCA9548A to switch to the current ADC
    tcaSelect(m_chan); // switches the MUX to whatever channel the loop is currently on (0 or 1)
    delay(5); // Small delay to allow the I2C bus to stabilize

    Serial.print("--- Reading MUX Channel ");
    Serial.print(m_chan);
    Serial.println(" ---");

    // 2. Loop through all 4 analog inputs on the active ADS1115
    // that loop counts from 0to 3 to read every pin on the currently selected ADC
    for (uint8_t adc_pin = 0; adc_pin < 4; adc_pin++) {
      int16_t raw_value = ads.readADC_SingleEnded(adc_pin);  // creates a 16-bit signed integer variable to hold the raw number from the ADC, 
      // then this triggers the active ADC to look at the specified pin (A0, A1, A2, A3), convert the analog voltage of the hall sensor
      // into a digital number, and return it. For a 16-bit ADC, this number will range from 0 to 32,767
      float voltage = ads.computeVolts(raw_value); // creates a decimal variable (float). the library calculates the mathematical
      // translation from that raw intege into an actual voltage

      

      // Print the output
      Serial.print("Sensor A");
      Serial.print(adc_pin);
      Serial.print(" -> Raw: ");
      Serial.print(raw_value);
      Serial.print(" | Voltage: ");
      Serial.print(voltage, 3);
      Serial.println(" V");
    }
    Serial.println(); 
  }

  delay(2000); // Wait 2 seconds before repeating the loop
}
