import re
import os
import RPi.GPIO as GPIO
import time
import pandas as pd
from paddleocr import PaddleOCR
from thefuzz import process

def NDC(data, dosage, unit,med):
    # Change directory
    os.chdir(r"/home/team31/project/AMD_code/ndcxls")

    # Import the NDC dataset
    filename = "filtered_product.csv"
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
    
def process_MGNDC(strings):
    for string in strings:
        if 'MG' in string:
            matches = re.findall(r'(\d+)[0oO]*MG', string)
            if matches:
                number_before_MG = matches[0]
                zeros_count = string[string.find(number_before_MG) + len(number_before_MG): string.find("MG")].count("0") + string[string.find(number_before_MG) + len(number_before_MG): string.find("MG")].count("o") + string[string.find(number_before_MG) + len(number_before_MG): string.find("MG")].count("O")
                result = number_before_MG + "0" * zeros_count
        
                return result

def process_MG(strings,med):
    for string in strings:
        if 'MG' in string:
            matches = re.findall(r'(\d+)[0oO]*MG', string)
            if matches:
                number_before_MG = matches[0]
                zeros_count = string[string.find(number_before_MG) + len(number_before_MG): string.find("MG")].count("0") + string[string.find(number_before_MG) + len(number_before_MG): string.find("MG")].count("o") + string[string.find(number_before_MG) + len(number_before_MG): string.find("MG")].count("O")
                result = number_before_MG + "0" * zeros_count 
                med.dose = result
                
                return
            
def process_TABLET(strings,med):
    for string in strings:
        if 'TABLET' in string:
            matches = re.findall(r'(\d+)\s*TABLET', string)
            if matches:
                number_before_TABLET = matches[0]
                result = number_before_TABLET 
                med.time = result
                
                return

def process_QTY(strings,med):
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

def imageocr(prescription):
    GPIO.setmode(GPIO.BCM)
    LEDs = 25
    GPIO.setup(LEDs, GPIO.OUT)

    GPIO.output(LEDs, GPIO.HIGH)
    time.sleep(2)
    fswebcam = 'fswebcam --resolution 1920x1080 --set "Focus, Automatic Continuous"=False --set "Focus, Absolute"=300 --crop 1000x1080+460+0 --save /home/team31/project/AMD_code/image.jpg'

    os.system(fswebcam)
    
    time.sleep(5)
    GPIO.output(LEDs, GPIO.LOW)
    GPIO.cleanup(LEDs)
    ocr_model = PaddleOCR(use_angle_cls=True, lang='en') # Initialize OCR model
    img_path = 'AMD_code/image.jpg'  # Path to the image file
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
    process_MG(data,prescription) 
    process_TABLET(data,prescription) 
    process_QTY(data,prescription)
    NDC(shortndc(data), process_MGNDC(data), 'MG',prescription) 
