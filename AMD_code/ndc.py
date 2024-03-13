import os
import pandas as pd
from thefuzz import process

# Change directory
os.chdir(r"/home/team31/project/AMD_code/ndcxls")

# Import the NDC dataset
filename = "product.csv"
dataset = pd.read_csv(filename)

queries = ['Tylneol', 'MOUTH EVERYO', 'CHRISTOPHER HO', 'ATORVASTATIN', 'TAKE1TABLETE', '0349518-178', 'N.M.D.RPi Hat', 'Y30', 'Walgreeks', 'Mtouirot', '(413)527-0777', '2024-03-09 15:32 (EST'] 
dosage = '10'
unit = 'Mg'

threshold = 85

matched_list = []

for query in queries:
  extract = process.extractOne(query, dataset["PROPRIETARYNAME"], score_cutoff=threshold)
  if extract is None:
    pass
  else:
    if str.upper(dosage) in str.upper(dataset.iloc[extract[2]]["ACTIVE_NUMERATOR_STRENGTH"]):
      if str.upper(unit) in str.upper(dataset.iloc[extract[2]]["ACTIVE_INGRED_UNIT"]):
        matched_list.append(extract[0])
  
print(matched_list)
