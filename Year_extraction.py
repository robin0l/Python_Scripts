# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 17:16:46 2023

@author: admin
"""

import pandas as pd
import re

def identify_patterns(input_text):
    patterns = [
        r"\b(\d{4}-\d{2})\b",       # ####-##
        r"\b(\d{4} to \d{4})\b",    # #### to ####
        r"\b(\d{4}to\d{4})\b",      # ####to####
        r"\b(\d{4} TO \d{4})\b",    # #### TO ####
        r"\b(\d{4}TO\d{4})\b",      # ####TO####
        r"\b(\d{4}-\d{4})\b",       # ####-####
        r"\b(\d{4}- \d{4})\b",      # ####- ####
        r"\b(\d{4} -\d{4})\b",      # #### -####
        r"\b(\d{4} - \d{4})\b",     # #### - ####
        r"\b(\d{4}\+)\b",           # ####+
        r"\b(19\d{2}|20\d{2})\b",   # ####
        r"\b(\d{2}-\d{2})\b",       # ##-##
        r"\b(\d{2} - \d{2})\b",
        r"\b(\d{2}-\d{4})\b",
        r"\b('\d{2}-\d{4})\b"       # ## - ##
    ]
    matches = []
    for pattern in patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        pattern_matches = regex.findall(input_text)
        matches.extend(pattern_matches)
    
    expanded_years = []
    for match in matches:
        if '-' in match or ' - ' in match:  # Updated condition to handle spaces around dash
            start_year, end_year = re.split(r'-| - ', match)
            if len(start_year) == 2:
                if int(start_year) <= 23:
                    start_year = '20' + start_year
                else:
                    start_year = '19' + start_year
            if len(end_year) == 2:
                if int(end_year) <= 23:
                    end_year = '20' + end_year
                else:
                    end_year = '19' + end_year
            expanded_years += [str(year) for year in range(int(start_year), int(end_year) + 1)]
        elif 'TO' in match.upper():
            year_range = match.split('TO')
            if len(year_range) == 1:
                year_range = match.split('to')
            if len(year_range) == 2:
                start_year, end_year = map(str.strip, year_range)
                if len(start_year) == 2:
                    if int(start_year) <= 23:
                        start_year = '20' + start_year
                    else:
                        start_year = '19' + start_year
                if len(end_year) == 2:
                    if int(end_year) <= 23:
                        end_year = '20' + end_year
                    else:
                        end_year = '19' + end_year
                expanded_years += [str(year) for year in range(int(start_year), int(end_year) + 1)]
            else:
                expanded_years.append(match)  # Consider it as a single year
        else:
            expanded_years.append(match)

    expanded_years = sorted(list(set(expanded_years)))  # Sort and remove duplicates
    
    # Filter out invalid years
    valid_years = []
    for year in expanded_years:
        try:
            if 0 <= int(year) <= 2025:  # Adjust the upper limit as needed
                valid_years.append(year)
        except ValueError:
            if not year.endswith('+'):  # Exclude patterns like '4000+'
                valid_years.append(year)

    expanded_years = sorted(list(set(valid_years)))  # Sort and remove duplicates

    return expanded_years if expanded_years else None

# Read the Excel file into a DataFrame
data = pd.read_excel(r'C:\Users\Admin\Desktop\Cover zone\analysis\Python Extract details\title input script.xlsx')

# Apply the identify_patterns function to each title in the DataFrame
data['Extracted Dates'] = data['Title'].apply(lambda x: identify_patterns(str(x)))

# Print the updated DataFrame with extracted dates
#print(data[['Title', 'Extracted Dates']])

data.to_excel(r'C:\Users\Admin\Desktop\Cover zone\analysis\Python Extract details\title input script-output.xlsx', index=False)
