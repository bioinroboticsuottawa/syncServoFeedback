const int analogInPin = A0;

int sensorValue = 0;

void setup() {  
    Serial.begin(9600);
    delay(50);
    while (!Serial.available()) {
      Serial.write("!");
      delay(300);
    }
    // read the byte that Python will send over
    Serial.read();
}

void loop() {
  if(Serial.available()) {
    uint8_t count = serial_busy_wait();
    for(uint8_t i = 0; i < count; i++) {
      int sensorValue = analogRead(analogInPin);
      char val[4];
      sprintf(val, "%4d,", sensorValue);
      Serial.print(val);
    }
    Serial.println();
    count = 0;
  }
}

char serial_busy_wait() {
  while(!Serial.available()) {
  // do nothing until ready
  }
  return Serial.read();
}

