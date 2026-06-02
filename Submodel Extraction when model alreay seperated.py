# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 11:14:03 2024

@author: admin
"""

import pandas as pd
import csv
import warnings

warnings.filterwarnings('ignore')

# Read the Excel files
make_model_df = pd.read_excel(r'D:\2024\Jan\Abhinav sharma\Lambretta\Lambretta MVL.xlsx')
makes_set = set(make_model_df['Make'])
models_set = set(make_model_df['Model'])

# Read the Excel files
title_df = pd.read_excel(r'D:\2024\Jan\Abhinav sharma\Lambretta\Lambretta_Model_out_put.xlsx')

def create_make_model_data(file_path):
    make_model_data = {}
    with open(file_path) as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for make, model, submodel in reader:
            make = make.upper()
            model = model.upper()
            submodel = submodel.upper()
            if make not in make_model_data:
                make_model_data[make] = {}
            if model not in make_model_data[make]:
                make_model_data[make][model] = set()
            make_model_data[make][model].add(submodel)
    return make_model_data

make_model_data = create_make_model_data(r'D:\2024\Jan\Abhinav sharma\Lambretta\Lambretta MVL Submodel CSV.csv')

def extract_submodel_from_columns(row):
    make = str(row['Make']).upper()
    model = str(row['Model']).upper()
    submodels = set()

    # Extract submodels from the 'Title' column using make and model as keys
    for make_key in makes_set.intersection([make]):
        for model_key in models_set.intersection([model]):
            relevant_submodels = make_model_data.get(make_key, {}).get(model_key, set())
            # Extract submodels with multiple words
            title = str(row['Title']).upper()
            words = title.split()
            for i in range(len(words)):
                for j in range(i + 1, len(words) + 1):
                    submodel = ' '.join(words[i:j]).upper()
                    if submodel in relevant_submodels:
                        submodels.add(submodel)

    return ', '.join(submodels) if submodels else ''

# Apply the updated extraction function to the DataFrame
title_df['Submodel'] = title_df.apply(extract_submodel_from_columns, axis=1)
title_df.to_excel(r'D:\as\2024\Jan\Abhinav sharma\Lambretta\Lambretta_Model_Submodel_out_put.xlsx', index=False)
