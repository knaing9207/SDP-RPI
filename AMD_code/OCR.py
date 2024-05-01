import re
import os
import RPi.GPIO as GPIO
import time
import serial
import pandas as pd
from paddleocr import PaddleOCR
from thefuzz import process

# Define the serial port
arduino_port = '/dev/ttyACM0'  # Change this to match your Arduino port
arduino_baudrate = 9600  # Make sure this matches the baud rate in your Arduino code

# Initialize serial communication with the Arduino
arduino = serial.Serial(arduino_port, arduino_baudrate, timeout=1)

# Function to send a string to the Arduino
def send_to_arduino(string):
    arduino.write(string.encode())  # Convert string to bytes and send

# Function to read a string from the Arduino
def read_from_arduino():
    return arduino.readline().decode().strip()  # Read line and decode from bytes

def NDC(data, dosage, unit, med):

    # Import the NDC dataset
    filename = "/home/team31/project/AMD_code/ndcxls/filtered_products.csv"
    dataset = pd.read_csv(filename)

    threshold = 85

    matched_list = []

    for query in data:
        extract = process.extractOne(query, dataset["PROPRIETARYNAME"], score_cutoff=threshold)
        if extract is None:
            pass
        else:
            if str.upper(dosage) in str.upper(dataset.iloc[extract[2]]["ACTIVE_NUMERATOR_STRENGTH"]):
                if str.upper(unit) in str.upper(dataset.iloc[extract[2]]["ACTIVE_INGRED_UNIT"]):
                    matched_list.append(extract[0])
                    result = matched_list[0]
                    med.name = result

                    return

def process_MG(strings, med):
    for string in strings:
        if 'MG' in string:
            matches = re.findall(r'(\d+)[0oO]*MG', string)
            if matches:
                number_before_MG = matches[0]
                zeros_count = string[string.find(number_before_MG) + len(number_before_MG): string.find("MG")].count("0") + string[string.find(number_before_MG) + len(number_before_MG): string.find("MG")].count("o") + string[string.find(number_before_MG) + len(number_before_MG): string.find("MG")].count("O")
                result = number_before_MG + "0" * zeros_count 
                med.dose = result
                
                return result
            
def process_QTY(strings, med):
    for string in strings:
        if 'QTY' in string:
            matches_with_space = re.findall(r'[QO0o]TY\s*[:;]?\s*(\d+)\s*([oO0]*)', string)
            matches_without_space = re.findall(r'[QO0o]TY[:;]?\s*(\d+)\s*([oO0]*)', string)
            matches = matches_with_space or matches_without_space
            if matches:
                number, zeros = matches[0]
                zeros_count = len(zeros)
                result = number + "0" * zeros_count
                med.qty = result
                
                return
            
def shortndc(input_array):
    new_array = []
    for item in input_array:
        if ' ' in item:
            split_items = item.split()  # Splitting the item based on spaces
            new_array.extend(split_items)  # Adding split items to the new array
        else:
            new_array.append(item)  # Adding items without spaces directly to the new array
    return new_array

def find_string_position (list, string):
    postion = list.index(string)
    return postion


def imageocr(prescription):
    GPIO.setmode(GPIO.BCM)
    LEDs = 25
    GPIO.setup(LEDs, GPIO.OUT)
    GPIO.output(LEDs, GPIO.HIGH)

    fswebcam = 'fswebcam --resolution 1920x1080 --set "Focus, Automatic Continuous"=False --set "Focus, Absolute"=300 --crop 1000x1080+460+0 --save /home/team31/project/AMDimages/image4.jpg'
    os.system(fswebcam)
    send_to_arduino("Pic 1\n")  # Send a string to the Arduino
    time.sleep(1)
    fswebcam = 'fswebcam --resolution 1920x1080 --set "Focus, Automatic Continuous"=False --set "Focus, Absolute"=300 --crop 1000x1080+460+0 --save /home/team31/project/AMDimages/image5.jpg'
    os.system(fswebcam)
    send_to_arduino("Pic 2\n")  # Send a string to the Arduino
    time.sleep(1)
    fswebcam = 'fswebcam --resolution 1920x1080 --set "Focus, Automatic Continuous"=False --set "Focus, Absolute"=300 --crop 1000x1080+460+0 --save /home/team31/project/AMDimages/image6.jpg'
    os.system(fswebcam)
    send_to_arduino("Pic 3\n")  # Send a string to the Arduino
    time.sleep(1)
    fswebcam = 'fswebcam --resolution 1920x1080 --set "Focus, Automatic Continuous"=False --set "Focus, Absolute"=300 --crop 1000x1080+460+0 --save /home/team31/project/AMDimages/image7.jpg'
    os.system(fswebcam)
    send_to_arduino("Pic 4\n")  # Send a string to the Arduino
    time.sleep(3)
    fswebcam = 'fswebcam --resolution 1920x1080 --set "Focus, Automatic Continuous"=False --set "Focus, Absolute"=300 --crop 1000x1080+460+0 --save /home/team31/project/AMDimages/image3.jpg'
    os.system(fswebcam)
    send_to_arduino("Pic 5\n")  # Send a string to the Arduino
    time.sleep(1)
    fswebcam = 'fswebcam --resolution 1920x1080 --set "Focus, Automatic Continuous"=False --set "Focus, Absolute"=300 --crop 1000x1080+460+0 --save /home/team31/project/AMDimages/image2.jpg'
    os.system(fswebcam)
    send_to_arduino("Pic 6\n")  # Send a string to the Arduino
    time.sleep(1)
    fswebcam = 'fswebcam --resolution 1920x1080 --set "Focus, Automatic Continuous"=False --set "Focus, Absolute"=300 --crop 1000x1080+460+0 --save /home/team31/project/AMDimages/image1.jpg'
    os.system(fswebcam)
    time.sleep(0.5)
    send_to_arduino("Pic 7\n")  # Send a string to the Arduino
    
    GPIO.output(LEDs, GPIO.LOW)
    GPIO.cleanup(LEDs)
    ocr_model = PaddleOCR(use_angle_cls=True, lang='en') # Initialize OCR model
    img_path = '/home/team31/project/AMDimages/image4.jpg'  # Path to the image file
    result = ocr_model.ocr(img_path, cls=True) # Perform OCR on the image

    text = []
    for item in result[0]: # Iterate through each item in the OCR result
        word = item[1][0] # Access the recognized text in each item and add it to the recognized_texts list
        text.append(word)

    data = [] # Print all the recognized text items
    for word in text:
        data.append(word)

    print(data)


    # Process the data using process_MG
    dose = process_MG(data, prescription)
    process_QTY(data, prescription)
    shortarray = shortndc(data)
    position = find_string_position(shortarray, "%sMG" % dose or "%s" % dose)
    namearray = shortarray[position-2:position]
    NDC(namearray, dose, 'MG', prescription)
