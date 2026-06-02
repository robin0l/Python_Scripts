import pandas as pd
import re

# Define the file path
file_path = r'C:\Users\Admin\Downloads\179258 260 exceeding limit python.xlsx'

# Load the Excel file
df = pd.read_excel(file_path)

# Define the column to manipulate
column_name = 'UK Data Cat 179852:Reference OE/OEM Number'

# Function to replace every 28th comma with a pipe
def replace_nth_comma_with_pipe(text, n):
    parts = text.split(", ")
    for i in range(n-1, len(parts), n):
        parts[i] = parts[i] + '|'
    return ", ".join(parts)

# Apply the pipe logic (if needed)
df[column_name] = df[column_name].apply(lambda x: replace_nth_comma_with_pipe(str(x), 28))

# Extract only the engine size (e.g., 2.0, 1.6) to a new column
def extract_engine_size(text):
    match = re.search(r'\d+\.\d+', str(text))
    return match.group(0) if match else None

df['Engine Size'] = df[column_name].apply(extract_engine_size)

# Save the modified DataFrame
output_path = r'C:\Users\Admin\Downloads\179258_260_exceeding_limit_python_modified.xlsx'
df.to_excel(output_path, index=False)

print(f"✅ Modified file saved to: {output_path}")

