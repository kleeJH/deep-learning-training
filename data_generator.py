import cv2
import csv
import os

def onMouse(event, x, y, flags, params):
        global mouseX, mouseY
        if event == cv2.EVENT_LBUTTONDOWN:
            print(" Clicked at X:{}, Y:{}".format(x, y))
            mouseX, mouseY = x, y
            return
        elif event == cv2.EVENT_RBUTTONDOWN:
            return

def record_click_positions(video_file_path, csv_file_path):
    current_image_number = 1
    cap = cv2.VideoCapture(video_file_path)

    # Check if video file opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Create a window to display the video and set Mouse Callback
    cv2.namedWindow("Video Player")
    cv2.setMouseCallback("Video Player", onMouse)

    # Create a CSV file to record click positions
    with open(csv_file_path, mode='w') as csv_file:
        fieldnames = ['img_number', 'x_position', 'y_position']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Read each frame of the video and display it to the user
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            cv2.imshow("Video Player", frame)

            # Wait for user to click somewhere in the frame
            key = cv2.waitKey(0)

            if key == ord('q'):  # Quit if 'q' is pressed
                break
            elif key == ord('c'):
                # Write click position to CSV file
                img_file_name =  "IMG_{:03d}.jpg".format(current_image_number)
                writer.writerow({'img_number': img_file_name,
                                 'x_position': mouseX,
                                 'y_position': mouseY})
                cv2.imwrite("./data/" + img_file_name, frame)
                current_image_number += 1
            elif key == ord('s'): # Skip
                continue

        # Release video capture and close CSV file and video window
        cap.release()
        cv2.destroyAllWindows()

record_click_positions("./video/sample.mp4", "./data/train.csv")