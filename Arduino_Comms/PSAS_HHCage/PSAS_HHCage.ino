#include <Adafruit_MMC56x3.h>
/* Assign a unique ID to this sensor at the same time */
Adafruit_MMC5603 mmc = Adafruit_MMC5603(12345);

//Assigning pins to variables
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
  // Setting pins as output. 
 pinMode(xina, OUTPUT);
 pinMode(xinb, OUTPUT);
 pinMode(yina, OUTPUT);
 pinMode(yinb, OUTPUT);
 pinMode(zina, OUTPUT);
 pinMode(zinb, OUTPUT);

 //Setting all pins off
 digitalWrite(xina,LOW);
 digitalWrite(xinb,LOW);
 digitalWrite(yina,LOW);
 digitalWrite(yinb,LOW);
 digitalWrite(zina,LOW);
 digitalWrite(zinb,LOW);
 
 //Baudrate/bytes per second set.
 Serial.begin(115200);

 Serial.println("Arduino Nano H-bridge Controller");

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
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);
  }
  if (incomingByte != 0){
  //Shutdown
  if (incomingByte == 'a'){
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
  //X Bridge Off character: 'b' Not working
  if (incomingByte == 'b'){
    digitalWrite(xina,LOW);
    digitalWrite(xinb,LOW);
    xstat = 0;
  }  
  //Y Bridge Off character: 'c' Not working
  if (incomingByte == 'c'){
    digitalWrite(yina,LOW);
    digitalWrite(yinb,LOW);
    ystat = 0;
  }  
  //Z Bridge Off character: 'd' Not working
  if (incomingByte == 'd'){
    digitalWrite(zina,LOW);
    digitalWrite(zinb,LOW);
    zstat = 0;
  }  
  //H-Bridge Status message
  if (incomingByte == 's'){
    Serial.print(xstat);
    Serial.print(ystat);
    Serial.println(zstat);
  }
  //mag Status message
  if (incomingByte == 'q'){
    Serial.println(magstat);
  }
  //positive "x"
  if (incomingByte == 'x'){
    digitalWrite(xinb,LOW);
    digitalWrite(xina,HIGH);
    xstat = 1;
  }
  //negative "X" Not working
  if (incomingByte == 'X'){
    digitalWrite(xina,LOW);
    digitalWrite(xinb,HIGH);
    xstat = 2;
  }
  //positive "y"
  if (incomingByte == 'y'){
    digitalWrite(yinb,LOW);
    digitalWrite(yina,HIGH);
    ystat = 1;
  }
  //negative "Y" Not working
  if (incomingByte == 'Y'){
    digitalWrite(yina,LOW);
    digitalWrite(yinb,HIGH);
    ystat = 2;
  }  
  //positive "z"
  if (incomingByte == 'z'){
    digitalWrite(zinb,LOW);
    digitalWrite(zina,HIGH);
    zstat = 1;
  }
  //negative "Z" Not working
  if (incomingByte == 'Z'){
    digitalWrite(zina,LOW);
    digitalWrite(zinb,HIGH);
    zstat = 2;
  }  
  //mag reading
  if (incomingByte == 'm'){
    sensors_event_t event;
    mmc.getEvent(&event);
    Serial.print(event.magnetic.x);
    Serial.print(",");
    Serial.print(event.magnetic.y);
    Serial.print(",");
    Serial.println(event.magnetic.z);
  }
  //temp reading
  if (incomingByte == 't'){
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
