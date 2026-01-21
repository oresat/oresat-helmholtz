void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(9600);
  delay(1000);
}

void loop() {
  // Serial.println("Starting loop");
  // put your main code here, to run repeatedly:
  if (Serial1.available() > 0) {
    Serial.println("Recieved a char, trying to print it");
    //char data = Serial1.read();
    Serial.write(Serial1.read());
  }
  if (Serial.available() > 0) {
    Serial.println("Sending a char");
    Serial1.write(Serial.read());
  }
  //delay(5);
}
