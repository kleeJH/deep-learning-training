import cv2
import csv
import os

PREDICTION_CSV_FILE_PATH = "./data/prediction/train.csv"
XY_LOCATE_CSV_FILE_PATH = "./data/xy_locate/train.csv"

try:
    if not os.path.exists('data/prediction'):
        os.makedirs('data/prediction')
except OSError:
    print('Error creating directory - data/prediction')

try:
    if not os.path.exists('data/xy_locate'):
        os.makedirs('data/xy_locate')
except OSError:
    print('Error creating directory - data/xy_locate')

def onMouse(event, x, y, flags, params):
        global mouseX, mouseY
        if event == cv2.EVENT_LBUTTONDOWN:
            print(" Clicked at X:{}, Y:{}".format(x, y))
            mouseX, mouseY = x, y
            return
        elif event == cv2.EVENT_RBUTTONDOWN:
            return

def record_click_positions(video_file_path, predict_model:bool=True):
    if predict_model:
        print("PREDICTION MODEL DATA GENERATOR: Press (1) for Truth=1, Press (0) for Truth=0, Press (s) to skip a frame, Press (q) to quit")
    else:
        print("XY LOCATE MODEL DATA GENERATOR: Press (left click on image and c) to record down the coordinate of the tag, Press (s) to skip a frame, Press (q) to quit")

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
    with open(PREDICTION_CSV_FILE_PATH if predict_model else XY_LOCATE_CSV_FILE_PATH, mode='w') as csv_file:
        if predict_model:
            fieldnames = ['img_number', 'truth']
        else:
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
            img_file_name =  "IMG_{:03d}.jpg".format(current_image_number)

            if predict_model:
                if key == ord('q'):  # Quit if 'q' is pressed
                    break
                elif key == ord('1'):
                    # Write click position to CSV file
                    writer.writerow({'img_number': img_file_name,
                                    'truth': 1,})
                    cv2.imwrite("./data/prediction/" + img_file_name, frame)
                    print("TRUTH")
                    current_image_number += 1
                elif key == ord('0'):
                    # Write click position to CSV file
                    writer.writerow({'img_number': img_file_name,
                                    'truth': 0,})
                    cv2.imwrite("./data/prediction/" + img_file_name, frame)
                    print("NO TRUTH")
                    current_image_number += 1
                elif key == ord('s'): # Skip
                    continue
            else:
                if key == ord('q'):  # Quit if 'q' is pressed
                    break
                elif key == ord('c'):
                    # Write click position to CSV file
                    writer.writerow({'img_number': img_file_name,
                                    'x_position': mouseX,
                                    'y_position': mouseY})
                    cv2.imwrite("./data/xy_locate/" + img_file_name, frame)
                    current_image_number += 1
                elif key == ord('s'): # Skip
                    continue
    
        # Release video capture and close CSV file and video window
        cap.release()
        cv2.destroyAllWindows()

record_click_positions("./video/sample.mp4", predict_model=False)