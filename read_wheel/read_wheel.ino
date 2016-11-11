const int NUM_OF_CASSETTES = 3;

void setup() {
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < NUM_OF_CASSETTES; i++) {
    // Print a comma before any value except from the first
    if (i != 0) {
      Serial.print(",");
    }
    Serial.print(analogRead(i));
  }
  // End the message with new line character
  Serial.println();
}

