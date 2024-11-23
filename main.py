import os
import sys
import cv2 as cv
import datetime as dt

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
    end = now.replace(hour=16, minute=52, second=30, microsecond=0)
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
            if is_it_worth_to_save():
                cv.imshow("Latest Image", image)
                save_image(image)
            else:
                print("It's not worth to save image at this time")
        else:
            print("Failed to read image from camera")
        key = cv.waitKey(time_delta)  # Wait for 5 minutes (300000 milliseconds)
        if key == ord("q"):
            cam.release()
            cv.destroyAllWindows()
            break

if __name__ == "__main__":
    automatic = not (sys.argv[1] == "manual") if len(sys.argv) > 1 else True
    time_delta = FIVE_MINUTES  # Default time delta is 5 minutes
    time_delta = int(sys.argv[2]) if len(sys.argv) > 2 else FIVE_MINUTES
    folder = sys.argv[3] if len(sys.argv) > 3 else "images/"
    print(f"Automatic: {automatic}")
    print(f"Time delta: {time_delta}")
    print(f"Folder: {folder}")
    set_count_by_images()
    if automatic:
        main_automatic(time_delta)
    else:
        main_manual()