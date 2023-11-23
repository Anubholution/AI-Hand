import Jetson.GPIO as GPIO
from hx711 import HX711

# Pin definitions
DT_PIN = 11  # BCM pin 22 for DT
SCK_PIN = 17  # BCM pin 23 for SCK

def clean_and_exit():
    GPIO.cleanup()
    print("Bye!")
    exit()

def setup():
    GPIO.setmode(GPIO.BCM)
    hx711 = HX711(dout=DT_PIN, pd_sck=SCK_PIN)
    hx711.set_offset(850000)  # Adjust this value based on your calibration
    hx711.set_scale(2280)    # Adjust this value based on your calibration
    return hx711

def read_weight(hx711):
    try:
        val = hx711.get_grams()
        print("Weight:", val, "grams")
    except KeyboardInterrupt:
        clean_and_exit()

if __name__ == "__main__":
    hx711 = setup()

    try:
        while True:
            read_weight(hx711)
    except KeyboardInterrupt:
        clean_and_exit()
