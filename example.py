import cv2
from gaze_tracking import GazeTracking
import csv
import matplotlib.pyplot as plt

gaze = GazeTracking()
webcam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap = cv2.VideoCapture('1.mp4')  # Replace 'your_video_file.mp4' with the path to your video file

# Check if the video file is opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("Total number of frames in the video:", frame_count)

cap.release()

import subprocess

video_path = '1.mp4'
subprocess.Popen(['start', '1.mp4'], shell=True)


csv_file = open("pupil_data.csv", mode='w', newline='')  # Open a CSV file for writing
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Left Pupil X", "Left Pupil Y", "Right Pupil X", "Right Pupil Y"])
z=0
while cap.read():
    # We get a new frame from the webcam
    ret, frame = webcam.read()
    frame=cv2.flip(frame,1)

    # Check if the frame is read successfully
    if not ret:
        print("Error: Could not read frame from USB camera.")
        break

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    z=z+1

    if left_pupil is not None and right_pupil is not None:
        print(left_pupil)
        print(right_pupil)
        csv_writer.writerow([left_pupil[0], left_pupil[1], right_pupil[0], right_pupil[1]])

    cv2.imshow("Demo", frame)

    key = cv2.waitKey(1)

    if z >= (frame_count/1.7):
        break

webcam.release()
csv_file.close()

# Read the data from the CSV file and plot it
data = []
with open("pupil_data.csv", mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        data.append([float(row[0]), float(row[1]), float(row[2]), float(row[3])])

# Separate the data into left and right pupils
left_pupil_x = [item[0] for item in data]
left_pupil_y = [item[1] for item in data]
right_pupil_x = [item[2] for item in data]
right_pupil_y = [item[3] for item in data]

# Plot the data
plt.figure(figsize=(10, 5))
plt.subplot(121)
plt.scatter(left_pupil_x, left_pupil_y, label='Left Pupil')
plt.xlabel('Left Pupil X')
plt.ylabel('Left Pupil Y')
plt.title('Left Pupil Data')

plt.axis([0, 260,300, 350])

plt.subplot(122)
plt.scatter(right_pupil_x, right_pupil_y, color='r', label='Right Pupil')
plt.xlabel('Right Pupil X')
plt.ylabel('Right Pupil Y')
plt.title('Right Pupil Data')
plt.axis([200, 450, 300, 400])
plt.legend()
plt.show()
