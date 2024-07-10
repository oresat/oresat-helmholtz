#include <Adafruit_MMC56x3.h>
/* Assign a unique ID to this sensor at the same time */
Adafruit_MMC5603 mmc = Adafruit_MMC5603(12345);

int xina = 6;
int xinb = 7;
int yina = 4;
int yinb = 5;
int zina = 2;
int zinb = 3;
int xstat = 0;
int ystat = 0;
int zstat = 0;
int magstat = 0;


int incomingByte = 0; // for incoming serial data

void setup() {
  // put your setup code here, to run once:
 pinMode(xina, OUTPUT);
 pinMode(xinb, OUTPUT);
 pinMode(yina, OUTPUT);
 pinMode(yinb, OUTPUT);
 pinMode(zina, OUTPUT);
 pinMode(zinb, OUTPUT);
 digitalWrite(xina,LOW);
 digitalWrite(xinb,LOW);
 digitalWrite(yina,LOW);
 digitalWrite(yinb,LOW);
 digitalWrite(zina,LOW);
 digitalWrite(zinb,LOW);
 Serial.begin(115200);
 
 
   // Initialise the mag sensor */
  if (mmc.begin(MMC56X3_DEFAULT_ADDRESS, &Wire)) {  // I2C mode
    magstat = 1;
    //mmc.printSensorDetails();
  }

}

void loop() {
  // put your main code here, to run repeatedly:
  
  // reply only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
  
    // say what you got:
    //  Serial.print("I received: ");
    //  Serial.println(incomingByte, DEC);
  }
  if (incomingByte != 0){
  //Shutdown
  if (incomingByte == 97){
    digitalWrite(xina,LOW);
    digitalWrite(xinb,LOW);
    digitalWrite(yina,LOW);
    digitalWrite(yinb,LOW);
    digitalWrite(zina,LOW);
    digitalWrite(zinb,LOW);
    xstat = 0;
    ystat = 0;
    zstat = 0;
  }  
  //X Bridge Off
  if (incomingByte == 98){
    digitalWrite(xina,LOW);
    digitalWrite(xinb,LOW);
    xstat = 0;
  }  
  //Y Bridge Off
  if (incomingByte == 99){
    digitalWrite(yina,LOW);
    digitalWrite(yinb,LOW);
    ystat = 0;
  }  
  //Z Bridge Off
  if (incomingByte == 100){
    digitalWrite(zina,LOW);
    digitalWrite(zinb,LOW);
    zstat = 0;
  }  
  //H-Bridge Status message
  if (incomingByte == 115){
    Serial.print(xstat);
    Serial.print(ystat);
    Serial.println(zstat);
  }
  //mag Status message
  if (incomingByte == 113){
    Serial.println(magstat);
  }
  //positive "x"
  if (incomingByte == 120){
    digitalWrite(xinb,LOW);
    digitalWrite(xina,HIGH);
    xstat = 1;
  }
  //negative "X"
  if (incomingByte == 88){
    digitalWrite(xina,LOW);
    digitalWrite(xinb,HIGH);
    xstat = 2;
  }
  //positive "y"
  if (incomingByte == 121){
    digitalWrite(yinb,LOW);
    digitalWrite(yina,HIGH);
    ystat = 1;
  }
  //negative "Y"
  if (incomingByte == 89){
    digitalWrite(yina,LOW);
    digitalWrite(yinb,HIGH);
    ystat = 2;
  }  
  //positive "z"
  if (incomingByte == 122){
    digitalWrite(zinb,LOW);
    digitalWrite(zina,HIGH);
    zstat = 1;
  }
  //negative "Z"
  if (incomingByte == 90){
    digitalWrite(zina,LOW);
    digitalWrite(zinb,HIGH);
    zstat = 2;
  }  
  //mag reading
  if (incomingByte == 109){
    sensors_event_t event;
    mmc.getEvent(&event);
    Serial.print(event.magnetic.x);
    Serial.print(",");
    Serial.print(event.magnetic.y);
    Serial.print(",");
    Serial.println(event.magnetic.z);
  }
  //temp reading
  if (incomingByte == 116){
    sensors_event_t event;
    mmc.getEvent(&event);
    float temp_c = mmc.readTemperature();
    Serial.println(temp_c);
  }
  //end of loop
  incomingByte = 0;
  Serial.flush();
}
}