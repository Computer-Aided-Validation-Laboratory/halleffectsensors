
const float VCC = 3.3;
const int sensor1= A0;
const int sensor2 = A1;
const int sensor3 = A2;
const int sensor4 = A3;
const int sensor5 = A4;
const int sensor6 = A5;


int data1, data2, data3, data4, data5, data6;

String dataLabel1 = "sensor1";
String dataLabel2 = "sensor2";
String dataLabel3 = "sensor3";
String dataLabel4 = "sensor4";
String dataLabel5 = "sensor5";
String dataLabel6 = "sensor6";


void setup() {
  Serial.begin(9600);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
  pinMode(sensor3, INPUT);
  pinMode(sensor4, INPUT);
  pinMode(sensor5, INPUT);
  pinMode(sensor6, INPUT);
  Serial.println("time_ms, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6");
}

void loop(){
 
  data1 = analogRead(sensor1);
  data2 = analogRead(sensor2);
  data3 = analogRead(sensor3);
  data4 = analogRead(sensor4);
  data5 = analogRead(sensor5);
  data6 = analogRead(sensor6);
  Serial.print(millis());
  Serial.print(",");
  Serial.print(data1);
  Serial.print(",");
  Serial.print(data2);
  Serial.print(",");
  Serial.print(data3);
  Serial.print(",");
  Serial.print(data4);
  Serial.print(",");
  Serial.print(data5);
  Serial.print(",");
  Serial.println(data6);

  delay(100); 
}
