int relayPins[] = {40,42,44,46,48,50,52};
int relays = 8;

void setup() {
  // the array elements are numbered from 0 to (pinCount - 1).
  // use a for loop to initialize each pin as an output:
  for (int thisPin = 0; thisPin < relays; thisPin++)  {
    pinMode(relayPins[thisPin], OUTPUT);      
  }
}

void loop() {
  // loop from the lowest pin to the highest:
  for (int thisPin = 0; thisPin < relays; thisPin++) {      // turn the pin on:     digitalWrite(ledPins[thisPin], HIGH);        delay(timer);                       // turn the pin off:     digitalWrite(ledPins[thisPin], LOW);       }   // loop from the highest pin to the lowest:   for (int thisPin = pinCount - 1; thisPin >= 0; thisPin--) {
    // turn the pin on:
    digitalWrite(relayPins[thisPin], HIGH);
    delay(3000);
    // turn the pin off:
    digitalWrite(relayPins[thisPin], LOW);
  }
}
