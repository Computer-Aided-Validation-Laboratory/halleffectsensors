# include <Wire.h>
# include <Adafruit_ADS1X15.h> 

# define TCA_ADDR 0x70
# define ADS_ADDR 0x48

const uint8_t NUM_ADCS = 2;

Adafruit_ADS1115 ads;

void tcaSelect(uint8_t channel) {
  if (channel > 7) return;
  Wire.beginTransmission(TCA9548A_ADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
 }

void setup() {
  Serial.begin(115200;
  Wire.begin();

  for (uint8_t = 0; i < NUM_ADCS; i++) {
    tcaSelect(i);
    if (!ads.begin(ADS1115_ADDR)) {
      Serial.print("error: ADC MUX ");
      Serial.println(i);
      while (1);
    }
    ads.setGain(GAIN_TWOTHIRDS);
  }

  Serial.print("Timestamp/ms");
  for (uint8_t adc_num = 0; adc_num < NUM_ADCS; adc_num++) {
    for (unit8_t pin = 0; pin < 4; pin++) {
      Serial.print(", ADC ");
      Serial.print(adc_num);
      Serial.print("_A");
      Serial.print(pin);
    }
  }
  Serial.println();
}

void loop() {
  unsigned long currentMillis = millis();
  Serial.print(currentMillis);

  for (uint8_t pin = 0; pin <4; pin++) {
    tcaSelect(adc_num);

    for (uint8_t pin = 0; pin < 4; pin++) {
      int16_t raw_adc = ads.readADC_SingleEnded(pin);

      Serial.print(",");
      Serial.print(raw_adc);
    }
  }
  Serial.println();

  delay(100);
}
