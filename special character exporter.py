import pandas as pd
import re
import os

# ====== CONFIGURATION ======
input_file = r'C:\Users\Admin\Downloads\python cleaning fitment\clean fitment.xlsx'
output_file = r'C:\Users\Admin\Downloads\python cleaning fitment\clean fitment_output_file.xlsx'

# ====== HELPER FUNCTION ======
def extract_engine_size(text):
    if pd.isna(text):
        return ""
    matches = re.findall(r'\b\d\.\d\b', str(text))  # Match only single-digit.x (e.g., 1.6, 2.0)
    return matches[0] if matches else ""

# ====== MAIN WORK ======
print("Loading file...")
df = pd.read_excel(input_file)

column_name = df.columns[0]  # Or manually set column name if needed

# Extract valid engine size numbers only
df['Extracted_EngineSize'] = df[column_name].apply(extract_engine_size)

# Save the result
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df.to_excel(output_file, index=False)

print(f"\n✅ Engine size extraction complete! Output saved at: {output_file}")
