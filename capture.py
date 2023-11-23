import cv2

def capture_with_key_press():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    image_count = 1  # Initialize image count

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture image")
            break

        cv2.imshow('Press Space to Capture', frame)
        
        key = cv2.waitKey(1)

        if key == 32:  # Spacebar key
            file_path = f"captured_image_{image_count}.jpg"  # Define file path with unique name
            cv2.imwrite(file_path, frame)
            print(f"Image saved to {file_path}")
            image_count += 1  # Increment image count for the next capture
        elif key == 27:  # ESC key
            print("Image capture canceled")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_with_key_press()
