import cv2
import datetime
import face_recognition
import os
import imageio
import sqlite3

# Set the path to ffmpeg executable
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"  # Update this path based on your ffmpeg installation

# Initialize camera
cap = cv2.VideoCapture(0)

# Create Objects_Images and Object_Gif_Images folders if they don't exist
if not os.path.exists('Objects_Images'):
    os.makedirs('Objects_Images')

if not os.path.exists('Object_Gif_Images'):
    os.makedirs('Object_Gif_Images')

# Create a connection and cursor for the SQLite database
conn = sqlite3.connect('object_database.db')
c = conn.cursor()

# Create a table to store object information if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS objects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number INTEGER,
                image_path TEXT,
                gif_path TEXT,
                time TEXT,
                date TEXT,
                day_name TEXT
            )''')

def save_to_database(serial_number, image_path, gif_path, time, date, day_name):
    # Insert data into the table
    c.execute('''INSERT INTO objects (serial_number, image_path, gif_path, time, date, day_name) 
                    VALUES (?, ?, ?, ?, ?, ?)''', (serial_number, image_path, gif_path, time, date, day_name))
    conn.commit()

# Flag to track waiting mode
waiting_mode = True

# Zoom factor
zoom_factor = 1.2

# List to store frames for the GIF
frames_for_gif = []

serial_number = 1

start_time = None

def process_frame(frame):
    global serial_number, waiting_mode, frames_for_gif, start_time

    # Perform facial recognition
    face_locations = face_recognition.face_locations(frame)

    if not face_locations:
        # No faces detected, continue with object detection

        # Perform object detection (replace this with your own logic or model)
        # objects = object_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # For demonstration purposes, let's assume an object is detected
        objects = [(50, 50, 100, 100)]  # Replace this with your object detection results

        if objects:
            # Something is moving, exit waiting mode
            waiting_mode = False

            for (x, y, w, h) in objects:
                # Zoom in on the detected object
                roi = frame[int(y - h * (zoom_factor - 1) / 2):int(y + h * (zoom_factor + 1) / 2),
                      int(x - w * (zoom_factor - 1) / 2):int(x + w * (zoom_factor + 1) / 2)]

                # Draw a rectangle around the detected object
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Add text to the image
                text = f'Serial: {serial_number}\nTime: {datetime.datetime.now().strftime("%H:%M:%S")}\n' \
                       f'Date: {datetime.datetime.now().strftime("%Y-%m-%d")}\nDay: {datetime.datetime.now().strftime("%A")}\n' \
                       f'Project: SkySnap_Object_Tracker\nCreated by: Ahmed Alzeidi, Software Engineering'

                # Put the text on the image
                cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

                # Save images
                cv2.imwrite(f'Objects_Images/object_{serial_number}_square.jpg', frame)
                cv2.imwrite(f'Objects_Images/object_{serial_number}_pointer.jpg', roi)
                cv2.imwrite(f'Objects_Images/object_{serial_number}_nothing1.jpg', frame)
                cv2.imwrite(f'Objects_Images/object_{serial_number}_nothing2.jpg', frame)
                cv2.imwrite(f'Objects_Images/object_{serial_number}_nothing3.jpg', frame)

                # Add frame to the list for the GIF
                frames_for_gif.append(frame.copy())  # Save a copy of the frame

                # Save data to the database
                save_to_database(serial_number, f'Objects_Images/object_{serial_number}_square.jpg', '',
                                 datetime.datetime.now().strftime("%H:%M:%S"),
                                 datetime.datetime.now().strftime("%Y-%m-%d"),
                                 datetime.datetime.now().strftime("%A"))

                serial_number += 1

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False

    return True

# Process frames until 'q' key is pressed
while process_frame(cap.read()[1]):
    if not waiting_mode and start_time is None:
        start_time = datetime.datetime.now()

    # Check if 5 seconds have passed since an object was detected
    if start_time is not None and (datetime.datetime.now() - start_time).total_seconds() >= 5:
        # Save GIF if frames are captured
        if frames_for_gif:
            gif_path = f'Object_Gif_Images/object_{serial_number - 1}_{start_time.strftime("%H-%M-%S")}_movement.gif'
            imageio.mimsave(gif_path, frames_for_gif, duration=0.1)

            # Update the database entry with the GIF path
            c.execute('''UPDATE objects SET gif_path = ? WHERE serial_number = ?''', (gif_path, serial_number - 1))
            conn.commit()

        # Reset variables for the next detection
        waiting_mode = True
        frames_for_gif = []
        start_time = None

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

# Close the connection to the database
conn.close()
