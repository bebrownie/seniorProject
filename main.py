import cv2
import picamera
import picamera.array

# Load the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier('path/to/haarcascade_frontalface_default.xml')

# Load the Haar cascade for eye detection
eye_cascade = cv2.CascadeClassifier('path/to/haarcascade_eye.xml')

# Initialize the camera
camera = picamera.PiCamera()

# Set the camera resolution
camera.resolution = (640, 480)

# Set the camera framerate
camera.framerate = 30

# Create an object for the video capture
video_capture = cv2.VideoCapture(0)

# Initialize the output array for the camera
output = picamera.array.PiRGBArray(camera, size=(640, 480))

# Allow the camera to warm up
camera.start_preview()
time.sleep(2)

# Loop through each frame from the video capture
while True:
    # Read the current frame
    ret, frame = video_capture.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Loop through each detected face
    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) for the face
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detect eyes in the face ROI
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Loop through each detected eye
        for (ex, ey, ew, eh) in eyes:
            # Draw a rectangle around the eye
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # Check if there are no eyes detected
        if len(eyes) == 0:
            print("Drowsiness detected!")

    # Show the frame
    cv2.imshow('frame', frame)

    # Clear the output array for the next frame
    output.truncate(0)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
