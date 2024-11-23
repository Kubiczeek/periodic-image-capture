# Periodic image capture
#### Made by [Kubiczeek](https://github.com/Kubiczeek)
This is a simple script that captures images from a webcam at a specified interval.
The images are saved by default in the `images` folder in the same directory as the script.
The script is written in Python and uses the OpenCV library to capture images from the webcam.
---
### Requirements
- Python 3
- OpenCV
---
### Running the script
The script has a few optional arguments that can be passed when running it:
`python main.py [-a] [-i INTERVAL] [-d DIRECTORY]`
- `-a` - If this flag is present, the script will run indefinitely, capturing images at the specified interval. If this flag is not present, the script will wait for these keys to be pressed:
> * `q` - Quit the script
> * `s` - Capture an image
> * `r` - Reset preview
> <br>
> Note: These commands only work when the `-a` flag is **not** present.
- `-i INTERVAL` - The interval at which the images are captured in milliseconds. The default value is 300 000 milliseconds (5 minutes).
- `-d DIRECTORY` - The directory where the images are saved. The default value is the `images` folder in the same directory as the script. 

#### Example usage:
- `python main.py -a -i 10000 -d my_images` - Capture images every 10 seconds and save them in the `my_images` folder.
- `python main.py -i 60000` - Image capture is set to manual mode. Images are saved in the `images` folder.
- `python main.py -d img/test/` - Image capture is set to manual mode. Images are saved in the `test` folder in the `img` folder.
- `python main.py` - Image capture is set to manual mode. Images are saved in the `images` folder.
- `python main.py -a -d D:/images` - Capture images every 5 minutes and save them in the `images` folder on the `D:` drive.