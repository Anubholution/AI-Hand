import serial
import time


def send_command(command):
    ser.write(','.join(map(str, command)).encode())  # Convert integers to string and join them with commas
    time.sleep(0.05)  # Allow some time for the Arduino to process the command

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        try:
            # Get user input as a space-separated list of integers
            #user_input = raw_input("Enter a list of integers (e.g., 1,2,3): ")
            # Convert the input to a list of integers
            #int_list = [int(x) for x in user_input.split(',')]
            #int_list = [7,8,6]
            #print(int_list)
            #print(type(int_list))
            # Send the list to the Arduino
            #send_command(int_list)

            # Read and print the response from the serial port
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            

            # Add a short delay before the next iteration
            time.sleep(0.01)

        except ValueError:
            print("Invalid input. Please enter integers separated by spaces.")
