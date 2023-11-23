#include <Servo.h>

const int maxSize = 10;  // Adjust the size based on your requirements
int receivedList[maxSize];
int index = 0;
Servo servoMotor;

void setup() {
  Serial.begin(9600);
  servoMotor.attach(9);  // Attach the servo to pin 9
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming data until a newline character is received
    String data = Serial.readStringUntil('\n');
    // Process the data
    processReceivedData(data);

    // Print the received values
    Serial.print("Received Values: ");
    for (int i = 0; i < index; i++) {
      Serial.print(receivedList[i]);
      Serial.print(" ");
    }
    Serial.println();

    // Control the servo in the loop
    if (index > 0) {
      int servoPosition = receivedList[0];
      // Map the received value to the servo range (adjust as needed)
      // int mappedPosition = map(servoPosition, 0, 1023, 0, 180);
      servoMotor.write(servoPosition);
      // Serial.print("Set Servo Position: ");
      // Serial.println(mappedPosition);
    }

    // Reset the index for the next iteration
    index = 0;

    // Add a delay if needed to control the update rate
    delay(100);
  }
}

void processReceivedData(String data) {
  // Parse the received data and save it into the array
  int value;
  char delimiter = ',';
  int startIndex = 0;
  int endIndex = data.indexOf(delimiter);

  while (endIndex != -1) {
    // Extract the substring between startIndex and endIndex
    String valueStr = data.substring(startIndex, endIndex);
    // Convert the substring to an integer
    value = valueStr.toInt();
    // Save the value into the array
    receivedList[index] = value;
    // Move to the next index
    index++;
    // Find the next delimiter in the string
    startIndex = endIndex + 1;
    endIndex = data.indexOf(delimiter, startIndex);
  }

  // Check if there is a value after the last delimiter
  if (startIndex < data.length()) {
    String lastValueStr = data.substring(startIndex);
    value = lastValueStr.toInt();
    receivedList[index] = value;
    index++;
  }
}