#include <Wire.h>
#include <Adafruit_ADS1X15.h>

#define TCA_ADDR 0x70
#define ADS_ADDR 0x48

const uint8_t NUM_ADCS = 4;

Adafruit_ADS1115 ads;

void tcaSelect(uint8_t channel) {
  if (channel > 7) return;

  Wire.beginTransmission(TCA_ADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

void setup() {

  Serial.begin(115200);
  Wire.begin();

  for (uint8_t adc_num = 0; adc_num < NUM_ADCS; adc_num++) {

    tcaSelect(adc_num);

    if (!ads.begin(ADS_ADDR)) {
      Serial.print("ERROR: ADS1115 not found on channel ");
      Serial.println(adc_num);
      while (1);
    }

    ads.setGain(GAIN_TWOTHIRDS);
  }

  Serial.print("time_ms");

  for (uint8_t adc_num = 0; adc_num < NUM_ADCS; adc_num++) {

    Serial.print(",ADC");
    Serial.print(adc_num);
    Serial.print("_A0");

    Serial.print(",ADC");
    Serial.print(adc_num);
    Serial.print("_A2");
  }

  Serial.println();
}

void loop() {

  unsigned long t = millis();

  Serial.print(t);

  for (uint8_t adc_num = 0; adc_num < NUM_ADCS; adc_num++) {

    tcaSelect(adc_num);

    delay(1);

    int16_t A0 = ads.readADC_SingleEnded(0);
    int16_t A2 = ads.readADC_SingleEnded(2);

    Serial.print(",");
    Serial.print(A0);

    Serial.print(",");
    Serial.print(A2);
  }

  Serial.println();

  delay(100);
}
