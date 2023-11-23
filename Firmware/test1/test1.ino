#include <Servo.h>

Servo myservo;
const int maxSize = 5;  // Adjust the size based on your requirements
int receivedList[maxSize];
int index = 0;
void setup() {
  Serial.begin(9600);
  myservo.attach(9);
}
void loop() {
  if (Serial.available() > 0) {
    // Read the incoming data until a newline character is received
    String data = Serial.readStringUntil('\n');
    // Process the data
    processReceivedData(data);
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
  // You can now use the receivedList array as needed
  // For example, print the received values to the Serial Monitor

    Serial.print("Received Value: ");
    Serial.println(receivedList[0]);
    myservo.write(receivedList[0]);                  // sets the servo position according to the scaled value
  delay(15);         
  
  // Reset the index for the next iteration
  index = 0;
}