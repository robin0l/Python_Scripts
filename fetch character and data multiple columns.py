import pandas as pd

# Function to transform the DataFrame
def transform_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Extract columns that are not Header or Data columns
    other_columns = [col for col in df.columns if not (col.startswith('Header') or col.startswith('Data'))]
    transformed_df = df[other_columns].copy()
    
    # Collect all unique header values
    headers = set()
    max_pairs = 25  # Adjust based on your actual number of pairs
    for i in range(max_pairs):
        header_col = f'Header.{i}'
        if header_col in df.columns:
            headers.update(df[header_col].dropna().unique())
    
    # Initialize new columns in the transformed DataFrame
    for header in headers:
        transformed_df[header] = None
    
    # Fill in the values for the new headers
    for i in range(max_pairs):
        header_col = f'Header.{i}'
        data_col = f'Data.{i}'
        if header_col in df.columns and data_col in df.columns:
            for index, row in df.iterrows():
                header_value = row[header_col]
                if pd.notna(header_value):
                    transformed_df.at[index, header_value] = row[data_col]
    
    
    return transformed_df

# File path to your Excel file
file_path = r'C:\Users\Admin\Downloads\details clean For ItemSpecifics.xlsx'

# Transform the data
transformed_df= transform_excel(file_path)

# Specify output file path
transformed_file_path = r'C:\Users\Admin\Downloads\details clean For ItemSpecifics_Output.xlsx'

# Save the transformed DataFrame to a new Excel file
transformed_df.to_excel(transformed_file_path, index=False)

print(f'Transformed data saved to {transformed_file_path}')