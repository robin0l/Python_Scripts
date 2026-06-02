# -*- coding: utf-8 -*-
"""
Updated on Thu Jul 27 16:41:18 2023

@updated_by: ChatGPT
"""

import pandas as pd
import re
import csv
import warnings

warnings.filterwarnings('ignore')

# Read the Make-Model Excel file
make_model_df = pd.read_excel(r'C:\Users\Admin\Desktop\Cover zone\analysis\Python Extract details\MVL MAKE MODEL SUB.xlsx')

# Convert Make and Model columns to sets
makes_set = set(make_model_df['Make'].str.upper())
models_set = set(make_model_df['Model'].str.upper())

# Read the title input Excel file
title_df = pd.read_excel(r'C:\Users\Admin\Desktop\Cover zone\analysis\Python Extract details\title input script.xlsx')

# Create dictionary for Make > Model > Submodel
def create_make_model_data(file_path):
    make_model_data = {}
    with open(file_path, encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
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

# Create dictionary
make_model_data = create_make_model_data(r'C:\Users\Admin\Desktop\Cover zone\analysis\Python Extract details\MVL MAKE MODEL SUB CSV.xlsx.csv')


# Extract Make
def extract_make(title):
    title = str(title).upper()
    makes = set()

    def is_word_in_title(word, title):
        return f' {word} ' in f' {title} ' or title.startswith(f'{word} ') or title.endswith(f' {word}') or title == word

    for make in makes_set:
        if is_word_in_title(make, title):
            makes.add(make)

    words = title.split()
    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            make = ' '.join(words[i:j])
            if make.upper() in makes_set and is_word_in_title(make, title):
                makes.add(make.upper())

    return ', '.join(sorted(makes)) if makes else ''


# Extract Model (updated logic)
def extract_model(args):
    title, make_model_data = args
    title = str(title).upper()
    makes = set()
    models = set()

    # Extract makes
    for make in makes_set:
        if make in title:
            makes.add(make)

    # Extract models
    words = title.split()
    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            model = ' '.join(words[i:j]).upper()
            if model in models_set:
                if makes:
                    for make in makes:
                        relevant_models_dict = make_model_data.get(make, {})
                        if model in relevant_models_dict:
                            models.add(model)
                else:
                    models.add(model)

    return ', '.join(sorted(models)) if models else ''


# Extract Submodel
def extract_submodel(args):
    title, make_model_data = args
    title = str(title).upper()
    makes = set()
    models = set()
    submodels = set()

    for make in makes_set:
        if make in title:
            makes.add(make)

    for model in models_set:
        if model in title:
            models.add(model)

    words = title.split()
    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            submodel = ' '.join(words[i:j]).upper()
            for make in makes:
                relevant_models = make_model_data.get(make, {})
                for model in models:
                    relevant_submodels = relevant_models.get(model, set())
                    if submodel in relevant_submodels:
                        submodels.add(submodel)

    return ', '.join(sorted(submodels)) if submodels else ''


# Apply the extraction logic
title_df['Make'] = title_df['Title'].apply(lambda x: extract_make(x))
title_df['Models'] = title_df.apply(lambda row: extract_model((row['Title'], make_model_data)), axis=1)
title_df['Submodel'] = title_df.apply(lambda row: extract_submodel((row['Title'], make_model_data)), axis=1)

# Save output
output_path = r'C:\Users\Admin\Desktop\Cover zone\analysis\Python Extract details\title input script_OUTPUT.xlsx'
title_df.to_excel(output_path, index=False)

print("Extraction complete. Output saved to:", output_path)
