import cv2
import time
from mailing import send_email
import os
import glob


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

# Make sure the images directory exists
if not os.path.exists("images"):
    os.makedirs("images")

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 0
image_with_object = None  # Initialize this variable outside the loop

while True:
    check, frame = video.read()
    
    if not check:
        break
        
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau
        continue

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 45, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Reset status for each frame
    status = 0
    
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
            
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        
        # Set status to 1 if motion is detected
        status = 1
        
        # Save the frame when motion is detected
        if status == 1:
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            if all_images:  # Check if there are any images
                index = int(len(all_images)/2)
                image_with_object = all_images[index]

    # Append the current status
    status_list.append(status)
    
    # Keep only the last two status values
    if len(status_list) > 2:
        status_list = status_list[-2:]

    # Check for the transition from motion to no motion
    if len(status_list) == 2 and status_list[0] == 1 and status_list[1] == 0:
        if image_with_object:
            print("Sending email...")
            send_email(image_with_object)
            clean_folder()
            image_with_object = None  # Reset the image variable

    print("Status List:", status_list)
    cv2.imshow("Video", frame)
    
    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()