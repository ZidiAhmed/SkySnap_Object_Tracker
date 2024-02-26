# SkySnap_Object_Tracker

SkySnap_Object_Tracker is a Python project that captures images and GIFs of objects detected in the sky using a camera. It employs face recognition to identify and stop capturing when humans or animals are detected. The captured images are stored in the `Objects_Images` folder, and GIFs are saved in the `Object_Gif_Images` folder. Additionally, the project utilizes SQLite for database storage to keep track of objects, including their serial number, image and GIF paths, time, date, and day name.

## Prerequisites

Before running the project, ensure you have the following dependencies installed:

- Python 3.x
- OpenCV (`pip install opencv-python`)
- Face Recognition (`pip install face_recognition`)
- ImageIO (`pip install imageio`)
- SQLite3 (Comes with Python standard library)

Make sure that the [ffmpeg](https://ffmpeg.org/download.html) executable is installed on your system, and set the correct path in the `main.py` file.

## Project Structure

The project directory structure should look like this:

```
SkySnap_Object_Tracker/
│
├── Object_Gif_Images/
├── Objects_Images/
├── main.py
└── object_database.db
```

## Usage

1. **Run the Script:**

   Open a terminal and navigate to the project directory:

   ```bash
   cd /path/to/SkySnap_Object_Tracker
   python main.py
   ```

2. **Stopping the Script:**

   Press 'q' in the terminal to stop capturing frames and close the application.

3. **Database:**

   The SQLite database `object_database.db` is created in the project directory. It stores information about each detected object.

## Additional Notes

- Make sure to customize the object detection logic in the script based on your specific requirements.

- Adjust the path to the `ffmpeg` executable in the `main.py` file according to your system.

- This project uses facial recognition to stop capturing when humans or animals are detected. Adjust this logic if needed.

- The script captures images continuously and starts recording GIFs when an object is detected. GIFs are saved in the `Object_Gif_Images` folder.

- Ensure you have proper permissions to write to the project directory.

## Author

- **Ahmed Alzeidi**
- Software Engineering

Feel free to customize, extend, or modify the code based on your project's requirements.
