
import streamlit as st
import serial
import time
st.set_page_config(layout ="wide")

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

def send_command():
    command = [st.session_state.servo_motor1 ,st.session_state.servo_motor2,st.session_state.stepper_revolution,st.session_state.stepper_speed ,st.session_state.stepper_direction]
    ser.write(','.join(map(str, command)).encode())

# Create a Streamlit app
st.title("AI Hand Master Controller")
# Center the title and increase its size using HTML and CSS
st.markdown(
    """
    <style>
        /* Center the title */
        div.stTitle {
            text-align: center;
        }
        /* Increase the size of the title */
        div.stTitle h1 {
            font-size: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize the first servo motor using st.session_state
if 'servo_motor1' not in st.session_state:
    st.session_state.servo_motor1 = 0

# Initialize the second servo motor using st.session_state
if 'servo_motor2' not in st.session_state:
    st.session_state.servo_motor2 = 0
if "stepper_revolution" not in st.session_state:
    st.session_state.stepper_revolution =0
if "stepper_speed" not in st.session_state:
    st.session_state.stepper_speed =0
if "stepper_direction" not in st.session_state:
    st.session_state.stepper_direction =0 

col1,col2 =st.columns(2)
with col1 :
    # Input fields for manual entry of values
    st.write("### Servo Motor 1:")
    manual_input_motor1 = st.number_input("Enter Servo Motor 1 Value:", value=st.session_state.servo_motor1)
    st.session_state.servo_motor1 = manual_input_motor1
    # send_command()

    st.write("### Servo Motor 2:")
    manual_input_motor2 = st.number_input("Enter Servo Motor 2 Value:", value=st.session_state.servo_motor2)
    st.session_state.servo_motor2 = manual_input_motor2

    st.write("### Stepper Motor:")
    manual_stepper_revolution = st.number_input("Enter stepper revolution Value:", value=  st.session_state.stepper_revolution)
    st.session_state.stepper_revolution = manual_stepper_revolution

    manual_stepper_speed = st.number_input("Enter stepper speed Value:", value=st.session_state.stepper_speed)
    st.session_state.stepper_speed = manual_stepper_speed

    manual_stepper_direction = st.toggle("stepper direction (clockwise )")
    st.stepper_direction = manual_stepper_direction
    

    send_command()

    # Display the current values of both servo motors
   


with col2:
    st.markdown('<style>div.Widget.row-widget.stRadio>div{flex-direction:row;}</style>', unsafe_allow_html=True)
    st.markdown(
        """
        <style>
            /* Style for the container of the information */
            div.container {
                padding: 10px;
                background-color: #F0F0F0;
                border-radius: 10px;
            }
            /* Style for headers */
            h3 {
                color: #333;
                font-size: 30px;
                margin-bottom: 8px;
            }
            /* Style for the information */
            p {
                font-size: 25px;
                margin-bottom: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h3>Servo Motors:</h3>', unsafe_allow_html=True)
    st.markdown(f'<p>Servo Motor 1: {st.session_state.servo_motor1}</p>', unsafe_allow_html=True)
    st.markdown(f'<p>Servo Motor 2: {st.session_state.servo_motor2}</p>', unsafe_allow_html=True)
    st.markdown('<h3>Stepper Motor:</h3>', unsafe_allow_html=True)
    st.markdown(f'<p>Revolution Value: {st.session_state.stepper_revolution}</p>', unsafe_allow_html=True)
    st.markdown(f'<p>Speed: {st.session_state.stepper_speed}</p>', unsafe_allow_html=True)
    st.markdown('<h3>Sensor data Readings:</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    placeholder=st.empty()
while True:
    
    try:
        
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(3)
        fsr_reading,asr_reading = map(int,line.split(","))

        with placeholder.container():
            st.write("Air Quality Sensor Reading :", asr_reading)
            st.write("Pressure Sensor Reading :", fsr_reading)
        time.sleep(3)
    except ValueError:
        pass
placeholder.empty()



