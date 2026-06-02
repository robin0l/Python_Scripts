# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:42:00 2023

@author: admin
"""


import pandas as pd

# Specify the paths to your Excel files
file_path1 = (r'C:\Users\admin\Desktop\for reference  template.xlsx')
file_path2 = (r'C:\Users\admin\Desktop\for reference LUK summary.xlsx')

# Read the Excel files into DataFrames
df2 = pd.read_excel(file_path1)
df1 = pd.read_excel(file_path2)

# Ensure that 'ABC' column contains string values
df1['ABC'] = df1['ABC'].astype(str)
df2['ABC'] = df2['ABC'].astype(str)

df1['ABC'] = df1['ABC'].str.strip()
df2['ABC'] = df2['ABC'].str.strip()

# Set 'Partnumber' as the index for both DataFrames
df2.set_index('ABC', inplace=True)
df1.set_index('ABC', inplace=True)

# Update values in df2 with corresponding values from df1
#df2.update(df1)
#df2['*Title'] = df1['*Title']
#df2['*Title'] = df2.index.map(df1['*Title'])
# Update values in df2 with corresponding values from df1
df2.update(df1)

# Reset the index to have 'Partnumber' as a regular column
df2.reset_index(inplace=True)

# Export the updated DataFrame to a new Excel file
output_file_path = r'C:\Users\admin\Desktop\for reference output.xlsx'
df2.to_excel(output_file_path, index=False)
