# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 10:43:22 2024

@author: JHON
"""

import pandas as pd
import numpy as np
from json import loads
import json
import os


def fill_dscrp(row):
    if not row['Description']:  # Check if the list is empty
       value = np.random.randint(1, 5)
       if value == 1:
           row['Description'] = [1]  # Assigning an array with only 1
       else:
           unique_values = set([value])
           additional_values = list(np.random.choice([2, 3, 4, 5], np.random.randint(1, 4), replace=False))
           unique_values.update(additional_values)
           row['Description'] = list(unique_values)
    return row

script_directory = os.path.dirname(os.path.abspath(__file__))
file_name = r"RA result_300_all_years.xlsx"
file_path = os.path.join(script_directory, file_name)

new_path = os.path.dirname(os.path.abspath(__file__))

df_randomized = pd.read_excel(file_path, sheet_name='Sheet1', header=0)

df_demographics = df_randomized[['Code','Age','Gender','Smoking']]
df_demographics ['Description'] = '' #creates a new empty column

df_demographics = df_demographics.apply(fill_dscrp, axis=1)

illness_dscrp = {1:'No known illness',2:'Hypertension',3:'Diabetes',4:'Arthiritis',5:'Cardio bypass'}

df_demographics['Description'] = df_demographics['Description'].apply(lambda x: [illness_dscrp[i] for i in x])
for i in range(len(df_demographics['Description'])):
    if df_demographics['Description'][i][0] == 'No known illness':
        joined_descrp = df_demographics['Description'][i][0]
    else:
        joined_descrp= 'History of '+', '.join(str(element) for element in df_demographics['Description'][i])
    df_demographics['Description'][i] = joined_descrp

df_demographics ['_id'] = ''

df_demographics ['_id'][0] = '63701d24f03239c72c00018e'
df_demographics ['_id'][1] = '63701d24f03239c72c00018f'
df_demographics ['_id'][2] = '63701d24f03239c72c000190'
df_demographics ['_id'][3] = '63701d24f03239c72c000191'
df_demographics ['_id'][4] = '63701d24f03239867500012a'
df_demographics ['_id'][5] = '63701d24f03239867500012b'

for i in range(6, 300):
    random_id = ''.join(np.random.choice(list('0123456789abcdef'), len(df_demographics['_id'][0])))
    df_demographics['_id'][i] = random_id

#df_to_dct = df_demographics.to_dict('records')

result_demogrphics = df_demographics.to_json(orient="records")
parsed_demographics = loads(result_demogrphics)

new_file = r'dataDemographics.json'
new_file_path = os.path.join(new_path, new_file)

with open(new_file_path, 'w') as json_file:
    json.dump(parsed_demographics, json_file, indent=2)
    
##Exporting the files into Excel
df_demographics.to_excel(new_path+'/'+r"dataDemographics.xlsx", index=False)