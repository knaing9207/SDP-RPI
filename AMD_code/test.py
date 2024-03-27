import re
import os
import time
import pandas as pd
from paddleocr import PaddleOCR
from thefuzz import process

def NDC(data, dosage, unit):
    # Change directory
    os.chdir(r"/home/team31/project/AMD_code/ndcxls")

    # Import the NDC dataset
    filename = "filtered_products.csv"
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
                    print(result)

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
            
def shortndc(input_array):
    new_array = []
    for item in input_array:
        if ' ' in item:
            split_items = item.split()  # Splitting the item based on spaces
            new_array.extend(split_items)  # Adding split items to the new array
        else:
            new_array.append(item)  # Adding items without spaces directly to the new array
    return new_array
            

data = ['TOBIAYENI', '123 S.MAIN ST', 'ROSWELL, NM 12345', 'ATORVASTATIN 10MG', 'TAKE1TABLETBY', 'MOUTHUP TO2 TIMES', 'DAILY ASNEEDED', 'QTY:30', 'OXJOHN L.M.D.', 'EFILL BEFORE:', '2/6/2023']

NDC(shortndc(data), process_MGNDC(data), 'MG') 