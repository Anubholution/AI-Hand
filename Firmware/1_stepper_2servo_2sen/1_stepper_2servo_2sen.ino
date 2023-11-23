#include<Servo.h>
Servo myservo;
Servo myser2;
#define dirPin 2
#define stepPin 3
const int maxSize = 5;  // Adjust the size based on your requirements
int receivedList[maxSize];
int index = 0;
int fsrPin = A3;  // FSR and 10K pulldown connected to A0
int fsrReading;   // Analog reading from the FSR resistor divider
int sensorPin = A0;  // Air quality sensor connected to A4
int sensorData;      // Analog reading from the air quality sensor
void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  myser2.attach(10);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}
void loop() {
  if (Serial.available() > 0) {
    // Read the incoming data until a newline character is received
    String data = Serial.readStringUntil('\n');
    // Process the data
    processReceivedData(data);
  }
  fsrReading = analogRead(fsrPin);
  sensorData = analogRead(sensorPin);
  String output = String(fsrReading) + "," + String(sensorData);
  // Print the string
  Serial.println(output);
  //delay(15);
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
  //fsrReading = analogRead(fsrPin);
  //sensorData = analogRead(sensorPin);
  //Serial.print("Received Value: ");
  myservo.write(receivedList[0]);

  myser2.write(receivedList[1]);  // sets the servo position according to the scaled value     //////////// servo_ange1, servo_ange2, stepper_revolution, stepper_speed, stepper_direction
    digitalWrite(dirPin, receivedList[4]);
    int speed = receivedList[2]*200;
  // Spin the stepper motor 1 revolution slowly:
  for (int i = 0; i < speed ; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(receivedList[3]);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(receivedList[3]);
  }
  //String output = String(fsrReading) + "," + String(sensorData);
// Print the string
  //Serial.println(output);
  //delay(15);
  // Reset the index for the next iteration
  index = 0;
}