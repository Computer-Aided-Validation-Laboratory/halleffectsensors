#include <Wire.h>
#include <Adafruit_ADS1X15.h>

#define TCA_ADDR 0x70
#define ADS_ADDR 0x48

const uint8_t NUM_ADCS = 3;

Adafruit_ADS1115 ads;

void tcaSelect(uint8_t channel) {
  if (channel > 7) return;

  Wire.beginTransmission(TCA_ADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

void setup() {

  Serial.begin(115200);
  Serial.println("BOOTING");
  delay(500);
  Wire.begin();

  // Check communication with each ADS1115
  for (uint8_t adc_num = 0; adc_num < NUM_ADCS; adc_num++) {

    Serial.print("Testing ADC ");
    Serial.println(adc_num);

    tcaSelect(adc_num);

    Serial.println("MUX selected");

    if (!ads.begin(ADS_ADDR)) {
      Serial.println("ADS FAILED");
      while(1);
    }

  Serial.println("ADS OK");
}
  ads.setGain(GAIN_TWOTHIRDS);

  // CSV header
  Serial.print("Timestamp_ms");

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

  unsigned long currentMillis = millis();

  Serial.print(currentMillis);

  for (uint8_t adc_num = 0; adc_num < NUM_ADCS; adc_num++) {

    tcaSelect(adc_num);

    delay(1);  // allow mux to settle

    int16_t raw_A0 = ads.readADC_SingleEnded(0);
    int16_t raw_A2 = ads.readADC_SingleEnded(2);

    Serial.print(",");
    Serial.print(raw_A0);

    Serial.print(",");
    Serial.print(raw_A2);
  }

  Serial.println();

  delay(100);
}
