
const float VCC = 5.0;
const int sensor1 = A0;
const int sensor2 = A1;
const int sensor3 = A2;
const int sensor4 = A3;

int data1, data2, data3, data4;

String dataLabel1 = "sensor1";
String dataLabel2 = "sensor2";
String dataLabel3 = "sensor3";
String dataLabel4 = "sensor4";

void setup() {
  Serial.begin(9600);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
  pinMode(sensor3, INPUT);
  pinMode(sensor4, INPUT);
  Serial.println("time_ms, sensor1, sensor2, sensor3, sensor4");
}

void loop() {
  data1 = analogRead(sensor1);
  data2 = analogRead(sensor2);
  data3 = analogRead(sensor3);
  data4 = analogRead(sensor4);
  Serial.print(millis());
  Serial.print(",");
  Serial.print(data1);
  Serial.print(",");
  Serial.print(data2);
  Serial.print(",");
  Serial.print(data3);
  Serial.print(",");
  Serial.print(data4);

  delay(100);
}
