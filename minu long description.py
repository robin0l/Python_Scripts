# -*- coding: utf-8 -*-
"""
Created on Wed May  8 09:34:52 2024

@author: Admin
"""

import pandas as pd
import html2text

# Replace 'your_file.xlsx' with the path to your Excel file
input_file_path = r'C:\Users\Admin\Downloads\Summary_pnts_input.xlsx'
output_file_path = r'C:\Users\Admin\Downloads\Summary_pnts_input_output.xlsx'   # Change as needed

# Replace 'column_name' with the actual column name containing HTML data
column_name = 'longdescription'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(input_file_path)

# Initialize the html2text converter
html_converter = html2text.HTML2Text()

# Set options for formatting
html_converter.body_width = 0  # Disable line wrapping
html_converter.wrap_links = False  # Disable link wrapping

# Function to convert HTML to formatted text
def html_to_formatted_text(html):
    if pd.notna(html) and isinstance(html, (str, int)):  # Check if the value is not NaN and is either a string or an integer
        return html_converter.handle(str(html))  # Convert to string before processing
    else:
        return ''  # Return an empty string for NaN values and non-string, non-integer values

# Apply the function to the specified column
df[column_name] = df[column_name].apply(html_to_formatted_text)

# Save the modified DataFrame to an Excel file
df.to_excel(output_file_path, index=False, engine='openpyxl')

print(f"Conversion completed. Output saved to {output_file_path}")