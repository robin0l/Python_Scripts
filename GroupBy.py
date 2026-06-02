import pandas as pd
# Specify the file path with 'r' for raw string to handle backslashes in Windows paths
file_path = r'C:\Users\Admin\Downloads\Combined group by data (2).xlsx'
# Read the Excel file
data = pd.read_excel(file_path)
# Convert 'Description' column to strings
data['features'] = data['features'].astype(str)
# Group the data by "ItemID" and aggregate the associated data
result = data.groupby('web')['features'].apply(','.join).reset_index()
# Save the result to a new Excel file
result.to_excel(r'C:\Users\Admin\Downloads\Combined group by data_output.xlsx', index=False)