int SENSOR_PIN = A0;

// Led is on when value is reached
int LED_IS_ON_VALUE = 300;

// Led is off again when value is reached
int LED_IS_OFF_VALUE = 150;

// If diff is larger than this value, led is changing
int EDGE_DETECTION_DIFF = 100;

bool led_is_on = false;
int lastValue = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int sensorValue = analogRead(SENSOR_PIN);
  int diff = sensorValue - lastValue;
//   Serial.print("Sensor read: ");
//   Serial.println(sensorValue, DEC);

//  if (diff > EDGE_DETECTION_DIFF) {
//    Serial.print("LED is turning ON. ");
//    Serial.print("value: ");
//    Serial.print(sensorValue, DEC);
//    Serial.print(" diff: ");
//    Serial.println(diff, DEC);
//  } else if (diff < -EDGE_DETECTION_DIFF) {
//    Serial.print("LED is turning OFF. ");
//    Serial.print("value: ");
//    Serial.print(sensorValue, DEC);
//    Serial.print(" diff: ");
//    Serial.println(diff, DEC);
//  }

  if (led_is_on && sensorValue < LED_IS_OFF_VALUE) {
    led_is_on = false;
    Serial.print("milliseconds: ");
    Serial.print(millis(), DEC);
    Serial.print(",Led is OFF");
    Serial.print(",sensorValue: ");
    Serial.print(sensorValue, DEC); 
  } else if (!led_is_on && sensorValue > LED_IS_ON_VALUE) {
    led_is_on = true;
    Serial.print("milliseconds: ");
    Serial.print(millis(), DEC);
    Serial.print(",Led is ON");
    Serial.print(",sensorValue: ");
    Serial.print(sensorValue, DEC);
  }

//  if (led_is_on && sensorValue < LED_IS_OFF_VALUE) {
//    led_is_on = false;
//    Serial.println("Led is OFF");  
//  } else if (!led_is_on && sensorValue > LED_IS_ON_VALUE) {
//    led_is_on = true;
//    Serial.println("Led is ON");  
//  }

//  if (sensorValue < 500 && toggle_high == true) {
//    Serial.print("Sensor read: ");
//    Serial.println(sensorValue, DEC);
//    Serial.println("Low value");
//    toggle_high = false;
//  } else if (sensorValue >= 500 && toggle_high == false) {
//    Serial.print("Sensor read: ");
//    Serial.println(sensorValue, DEC);
//    Serial.println("High value");
//    toggle_high = true;
//  }
//  Serial.print("Reading: ");
//  Serial.print(sensorValue, DEC);
//  Serial.print(" diff: ");
//  Serial.println(diff, DEC);
  lastValue = sensorValue;
  delay(10);
}
