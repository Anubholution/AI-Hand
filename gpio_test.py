import RPi.GPIO as GPIO
import serial 
import time



def extract_and_append(data, value1, value2):
    # Find the position of the first digit in the string
    start_index = next((i for i, c in enumerate(data) if c.isdigit()), None)

    # If a digit is found, extract the numeric value
    if start_index is not None:
        end_index = start_index + 1
        while end_index < len(data) and data[end_index].isdigit():
            end_index += 1
        numeric_value = int(data[start_index:end_index])

        # Append to the appropriate variable based on the starting character
        if data.startswith('A'):
            value1.pop()
            value1.append(numeric_value)
        elif data.startswith('F'):
            value2.pop()
            value2.append(numeric_value)


value1 = [200]
value2 = [300]
led_pin = 12 
GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
GPIO.setup(led_pin, GPIO.OUT)  # LED pin set as output
# Initial state for LEDs:
GPIO.output(led_pin, GPIO.LOW)
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

while True:
    try:
        data = arduino.readline()
        if data:
            extract_and_append(data, value1, value2)
            air_quality = int(value1[-1])
            force_sensor_resistance = int(value2[-1])
            print(data)
            #print(air_quality,force_sensor_resistance)
            if air_quality > 300:
                print("Not Safe for Human Working Conditions")
            if force_sensor_resistance > 300 :
                GPIO.output(led_pin, GPIO.HIGH)
            else:
                GPIO.output(led_pin, GPIO.LOW)
    except:
        arduino.close() 
        GPIO.cleanup()


