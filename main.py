import os
import cv2 as cv
import datetime as dt

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
    image_count = len(os.listdir(folder))

def main() -> None:
    result, image = cam.read()
    if result:
        cv.imshow("Image", image)
    else:
        print("Failed to read image from camera")
    while True:
        r, i = cam.read()
        if r:
            cv.imshow("ImageLive", i)
        key = cv.waitKey(1)
        if key == ord("q"):
            cam.release()
            cv.destroyAllWindows()
            break
        elif key == ord("s"):
            save_image(image)
            main()
            break
        elif key == ord("r"):
            main()
            break

if __name__ == "__main__":
    set_count_by_images()
    main()