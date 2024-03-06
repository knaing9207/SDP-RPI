import os
import cv2

while True:
    user = input("Take Picture?: (yes/no) ")
    if user == "yes":
        fswebcam = 'fswebcam --resolution 1920x1080 --save /home/team31/project/AMD_code/image.jpg'
        os.system(fswebcam)

       