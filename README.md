# AI-Hand
AI-Hand Project
Overview
The AI-Hand project integrates the Intel RealSense camera for depth sensing and the YOLO (You Only Look Once) model for object detection and inference. This combination enables the system to perceive its environment and make real-time decisions based on the detected objects.

# System Components
1. Hardware Components
Jetson Nano: The core processing unit for running the AI models and managing the system.
Intel RealSense Camera: Utilized for depth perception and capturing RGB data.
2. Software Components
Operating System: The system operates on a custom image backup for Jetson Nano dated November 23, 2023.

Backup Image Link: https://drive.google.com/file/d/1MUmnEWIxHewFUYagGNBTmIVu7_iS1JhV/view?usp=sharing
Virtual Environment Activation:
To activate the environment, run the following command:

$ source yolov5/Python-3.8.12/yolo/bin/activate
Libraries:
The environment includes necessary libraries, with a focus on YOLO model dependencies.

# Intel RealSense Integration
The Intel RealSense camera is employed to enhance the system's perception capabilities through depth sensing. The depth information is crucial for accurate object detection and understanding the spatial layout of the surroundings.

# Setup Instructions:
Connect the Intel RealSense camera to the designated port on the Jetson Nano.
Ensure the RealSense SDK is installed on the system for proper camera communication.
YOLO Model for Object Detection
The YOLO model is utilized for real-time object detection, allowing the system to identify and track objects within its field of view.

# Integration Steps:
Activate the virtual environment using the provided command.
Load the YOLO model and necessary dependencies within the virtual environment.
Configure the system to receive input from the Intel RealSense camera.
Implement the inference pipeline to process the camera feed and detect objects.
Usage
The integrated system, with the Intel RealSense camera and YOLO model, is now capable of real-time object detection and depth-informed decision-making.
