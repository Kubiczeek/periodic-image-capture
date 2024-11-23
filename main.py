import os
import sys
import cv2 as cv
import datetime as dt
import argparse

automatic = False
FIVE_MINUTES = 5*60*1000
folder = "images/"
image_count = 0

cam_port = 0
cam = cv.VideoCapture(cam_port)

def save_image(img: cv.Mat) -> None:
    global image_count
    if not os.path.exists(folder):
        os.makedirs(folder)
    image_name = f"image{image_count}-{dt.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.jpg"
    print(f"Saving image as {image_name}")
    if cv.imwrite(folder + image_name, img):
        print(f"Image saved successfully as {image_name}")
    else:
        print(f"Failed to save image as {image_name}")
    image_count += 1

def set_count_by_images() -> None:
    global image_count
    if not os.path.exists(folder):
        os.makedirs(folder)
    image_count = len(os.listdir(folder))

def is_it_worth_to_save() -> bool:
    # Returns true if the time is between 7.30 and 17.00
    now = dt.datetime.now()
    start = now.replace(hour=7, minute=30, second=0, microsecond=0)
    end = now.replace(hour=17, minute=00, second=0, microsecond=0)
    print(f"Current time: {now}")
    print(f"Start time: {start}")
    print(f"End time: {end}")
    if start <= now <= end:
        return True
    else:
        return False

def main_manual() -> None:
    result, image = cam.read()
    if result:
        cv.imshow("Latest Image", image)
    else:
        print("Failed to read image from camera")
    while True:
        r, i = cam.read()
        if r:
            cv.imshow("Live Camera", i)
        key = cv.waitKey(1)
        if key == ord("q"):
            cam.release()
            cv.destroyAllWindows()
            break
        elif key == ord("s"):
            save_image(image)
            main_manual()
            break
        elif key == ord("r"):
            main_manual()
            break

# automatic mode saves images automatically without user input every 5 minutes
def main_automatic(time_delta : int = 5*60*1000) -> None:
    while True:
        result, image = cam.read()
        if result:
            # Add text to the image with the time gap when images are being saved
            font = cv.FONT_HERSHEY_SIMPLEX
            text_time_window = "Images are saved every 5 minutes between 7.30 and 17.00"
            cv.putText(image, text_time_window, (10, 30), font, 0.5, (0, 0, 255), 1, cv.LINE_AA)
            if is_it_worth_to_save():
                text = "Image successfully saved - " + dt.datetime.now().strftime('%H:%M:%S %d.%m.%Y')
                cv.putText(image, text, (10, 60), font, 0.75, (0, 255, 0), 2, cv.LINE_AA)
                save_image(image)
            else:
                # Add text to the image, that it was not worth to save with the current time and date
                text = "Image not saved - " + dt.datetime.now().strftime('%H:%M:%S %d.%m.%Y')
                cv.putText(image, text, (10, 60), font, 0.75, (0, 0, 255), 2, cv.LINE_AA)
                print("It's not worth to save image at this time")
            cv.imshow("Latest Image", image)
        else:
            print("Failed to read image from camera")
        key = cv.waitKey(time_delta)  # Wait for 5 minutes (300000 milliseconds)
        if key == ord("q"):
            cam.release()
            cv.destroyAllWindows()
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Periodic image capture")
    parser.add_argument("-a", "--automatic", action="store_true", help="Enable automatic mode")
    parser.add_argument("-i", "--interval", type=int, default=FIVE_MINUTES, help="Interval between captures in milliseconds")
    parser.add_argument("-d", "--directory", type=str, default="images/", help="Directory to save images")

    args = parser.parse_args()

    automatic = args.automatic
    time_delta = args.interval
    folder = args.directory

    if folder[-1] != "/":
        folder += "/"

    print(f"Automatic: {automatic}")
    print(f"Time delta: {time_delta}")
    print(f"Folder: {folder}")
    set_count_by_images()
    if automatic:
        main_automatic(time_delta)
    else:
        main_manual()