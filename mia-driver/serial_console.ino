char buffer[255];
char bufferext[255];
int my_index = 0; // The injected board definitions use the variable name "index" so this has to be "my_index"
bool user_mode = true;

/**
* Serial is 9600 baud
* Line terminator is /r
* Delete (0x7f) is backspace
* No self-echo
* If you use the arrow keys it'll break so don't 
**/

void user_term() {
  // Check for bytes on serial:
  if (Serial.available() > 0) {
    // Read into buffer at index and echo to serial
    buffer[my_index] = Serial.read();
    Serial.print(buffer[my_index]);

    if (buffer[my_index] == '\r'){ // Special Case: Intercept carriage return (Enter)
      // Go to start of next line
      Serial.print("\r\n");
      // Null-terminate buffer and print as null-terminated string
      buffer[my_index] = '\0';
      if (strncmp(&(buffer[0]), "cali", 255) == 0){
        Serial.println("Calibration requested");
        // Implement calibration
        Serial.println(poll_magnetometer());
      } else if (strncmp(&(buffer[0]), "blsk", 255) == 0) {
        Serial.println("Entering Basalisk mode. This is designed to be controlled by automation, if you are a user type `exit` to quit.");
        user_mode = false;
        my_index = 0;
        return;
        // Implement Basalisk Mode
        // Implement Debugging
        // Maybe some ANSI codes?
      } else if (strncmp(&(buffer[0]), "help", 255) == 0) {
        Serial.println("Commands: ");
        Serial.println("cali - Begin a calibration sweep. This must be run before operating the helmholtz cage");
        Serial.println("blsk - Exit console mode and enter automated operation for interfacing with basalisk");
        Serial.println("stat - Display system status");
        Serial.println("help - Print this message");
      } else {
        Serial.print(&(buffer[0]));
        Serial.println(" is an invalid command!");
      }
      // Print prompt and reset index
      Serial.print("\r\n> ");
      my_index = 0;
    } else if ((int)buffer[my_index] == 127) { // Special Case: Intercept delete (Backspace) 
      // Decrement buffer pointer and blank the deleted character
      my_index--;
      Serial.print("\b \b");
    } else {
      my_index++;
    }
  }
}

void blsk_term() {
  String read = Serial.readStringUntil('\r');

  if (read == "exit") {
    user_mode = true;
    Serial.print("\r\n> ");
  }

  Serial.print("BASALISK DEBUG: Got ");
  Serial.println(read);
}

String poll_magnetometer() {
  Serial1.write('r');
  return Serial1.readStringUntil('\r');
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(9600);
  while(!Serial.available()){} // Wait for user input
  Serial.print("___  ____ ____ ____ \r\n|__] [__  |__| [__  \r\n|    ___] |  | ___]\r\n\nHelmholtz Controller\r\nv0.0.1\r\nType help for commands or cali to begin calibration.\r\n> ");
}

void loop() {
  if (user_mode) {
    user_term();
  } else {
    blsk_term();
  }
  
  if (Serial1.available()) {
    Serial1.readBytes(bufferext, 255);
    Serial.print(bufferext);
  }
}
