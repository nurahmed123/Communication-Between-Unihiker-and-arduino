int ledPin = 13;  // Pin 13 is connected to the built-in LED
String command;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);  // Begin serial communication
}

void loop() {
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');  // Read the incoming command
    
    if (command == "ON") {
      digitalWrite(ledPin, HIGH);  // Turn LED on
    } 
    else if (command == "OFF") {
      digitalWrite(ledPin, LOW);  // Turn LED off
    }
  }
}

