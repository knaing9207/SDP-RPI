#!/usr/bin/env python
# coding: utf-8

# In[2]:


from paddleocr import PaddleOCR,draw_ocr
from matplotlib import pyplot as plt # plot images
import os # folder directory navigation
import RPi.GPIO as GPIO
import time




def imageocr():
    
    GPIO.setmode(GPIO.BCM)
    LEDs = 25
    GPIO.setup(LEDs, GPIO.OUT)

    GPIO.output(LEDs, GPIO.HIGH)

    fswebcam = 'fswebcam --resolution 1920x1080 --save /home/team31/project/AMD_code/image.jpg'
    os.system(fswebcam)
    
    time.sleep(5)
    GPIO.output(LEDs, GPIO.LOW)
    GPIO.cleanup(LEDs)

    # In[3]:


    ocr_model = PaddleOCR(use_angle_cls=True, lang='en')


    # In[146]:


    # img_path = os.path.join('/home/team31/project/AMD_code', 'image.jpg')
    img_path = 'AMD_code/image.jpg'
    result = ocr_model.ocr(img_path)
    use_dilation=True


    # In[147]:


    data = []
    num = 0
    for res in result:
        for line in res:
            if num%2 !=0:
                data.append(line[0])
            num = num+1
    print(data)

    def make_list(strh):
        list2 = []
        for look in strh:
            list2.append(look)
        return list2

    def get_dosage(strh,ID):
        sen = strh.split(" ")
        index = sen.index(ID)
        if len(sen[index])>2:
            value = ""
            num1 = 0
            for wrdh in sen:
                if ID in wrdh:
                    value = sen[num1] + ID
                num1 = num1 +1
        elif len(sen[index]) == 2:
            value = sen[index-1]   

        return value

    def get_quantity(strh):
        #value = ""
        if ":" in strh:
            strh = strh.split(":")
            word2 = strh[1]
            value = word2 + " Tablets"
        else:
            word2 = ""
            q_list = make_list(strh)
            index = q_list.index("Y")
            length = len(q_list)
            for num in range(index+1,length):
                word2 = word2 + q_list[num]
            value = word2 + " Tablets"
        return value
        
    def get_directions(strh):
            sen = strh.split(" ")
            keyword = sen[0]
            length = len(keyword)
            if length == 4:
                word = sen[1]
                value = "Take " + word + " tablet(s) Everyday"
            elif length > 4:
                for letter in keyword:
                    if letter == "1" or letter =="2":
                        word = letter
                value = "Take " + word + " tablet(s) daily"
            return value


    # In[145]:


    #Looking for quantity,instruction,dosage,duration
    #Key Word: QTY,TAKE,MG,BEFORE
    quantity=""
    directions=""
    dosage=""
    duration=""


    for item in data:
        
        if "TAKE"  in item:
            directions = get_directions(item)
            print(f"Directions:{directions}")
            
        elif "QTY" in item:
            quantity = get_quantity(item)
            print(f" Quantity: {quantity}")
            
        elif "MG" in item:
            dosage = get_dosage(item,"MG")
            print(f"Dosage: {dosage} MG Tablets ")
        elif "MCG" in item:
            dosage =get_dosage(item,"MCG")
            print(f"Dosage: {dosage} MCG Tablets")
        elif "/" in item:
            duration = item
            print(f"Duration: {duration}")
        
        file1 = open("Information_Storage.txt","w")
        l = [directions+"\n",quantity+"\n",dosage+"\n",duration]
        file1.writelines(l)
        

