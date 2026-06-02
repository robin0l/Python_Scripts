# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:52:16 2024

@author: Admin
"""

import pandas as pd
import requests

# Function to fetch link from TecDoc API
def get_link(part_number):
    api_key = 'https://catalog-files.tecalliance.services/AzyKoWCh9tXQYtXSCcJc8/config.json'
    url = f'https://api.tecdoc.net/pegasus/rest/3/rd/article/findByNumber/{""}'
    headers = {'Accept': 'application/json', 'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Extract link or other relevant information from the response
        if data['data']:
            return data['data'][0]['link']
    return None
file_path = r'C:\Users\Admin\Downloads\scrape for links with api.xlsx'
# Read part numbers from Excel file
df = pd.read_excel(file_path)

# Add a new column for links
df['TecDoc_Link'] = ''

# Iterate over each part number and fetch the link
for index, row in df.iterrows():
    part_number = row['PartNumber']
    link = get_link(part_number)
    if link:
        df.at[index, 'TecDoc_Link'] = link

# Save the updated DataFrame to a new Excel file
df.to_excel(r'C:\Users\Admin\Downloads\scrape for links with api_output.xlsx', index=False)
