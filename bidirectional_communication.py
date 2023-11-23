'''
import serial
import time

# Serial port configuration
port = "/dev/ttyUSB0" # Corrected port name
baudrate = 9600
bytesize = serial.EIGHTBITS
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE
timeout = 5
xonxoff = False
rtscts = False
dsrdtr = False
writeTimeout = 2

# Open the serial port
arduino = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, dsrdtr, writeTimeout)

while True:
    try:
        arduino.write("Command from Jetson|".encode())
        data = arduino.readline()
        if data:
            print(data.decode())  # Assuming data is bytes, decode to string
        time.sleep(1)
    except Exception as e:
        print(e)
'''
import serial
import time

# Serial port configuration
port = "/dev/ttyUSB0"  # Corrected port name
baudrate = 9600
bytesize = serial.EIGHTBITS
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE
timeout = 1
xonxoff = False
rtscts = False
dsrdtr = False
writeTimeout = 1

# Open the serial port
arduino = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, dsrdtr, writeTimeout)
delimiter ="|"
def send_command(command):
    arduino.write(','.join(map(str, command))+ delimiter.encode())  # Convert integers to string and join them with commas
    time.sleep(0.05)  # Allow some time for the Arduino to process the command

while True:
    try:
        # Get user input as a comma-separated list of integers
        user_input = raw_input("Enter a list of integers (e.g., 1,2,3): ")
        # Convert the input to a list of integers
        int_list = [int(x) for x in user_input.split(',')]
        # Send the list to the Arduino
        send_command(int_list)
        
        data = arduino.readline()
        if data:
            print(data.decode())  # Assuming data is bytes, decode to string
    except Exception as e:
        print(e)



#aurdino code for 2 servo-motor 
'''
include <Servo.h>
Servo myservo;
Servo myser2;
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
  fsrReading = analogRead(fsrPin);
  sensorData = analogRead(sensorPin);
  Serial.print("Received Value: ");
  myservo.write(receivedList[0]);
  myser2.write(receivedList[1]);  // sets the servo position according to the scaled value
  String output = String(fsrReading) + "," + String(sensorData);
// Print the string
  Serial.println(output);
  delay(15);
  // Reset the index for the next iteration
  index = 0;
}'''