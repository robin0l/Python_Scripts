import pandas as pd
import re

def clean_text(text):
    if pd.isna(text):
        return text
    text = str(text)
    
    # Remove all line breaks (without adding commas)
    text = re.sub(r'[\r\n]+', '|', text)
    
    # Remove multiple spaces, tabs, and non-breaking spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Trim leading and trailing spaces
    text = text.strip()
    
    return text

# Read the Excel file
file_path = r'C:\Users\Admin\Downloads\HTML line breaker remove.xlsx'
df = pd.read_excel(file_path)

# Clean the entire DataFrame
df = df.applymap(clean_text)

# Write the cleaned DataFrame to a new Excel file
output_path = r'C:\Users\Admin\Downloads\HTML line breaker remove output.xlsx'
df.to_excel(output_path, index=False)

print("Completed. Line breaks removed, text combined in a cluster.")
