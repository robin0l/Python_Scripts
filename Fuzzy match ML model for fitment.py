import pandas as pd
from rapidfuzz import process, fuzz
import os

# ====== CONFIGURATION ======

# Input your file paths here (directly hardcoded)
scraped_file_path = r'C:\Users\Admin\Downloads\python cleaning fitment\fuzzy_match_scraped.xlsx'
mvl_file_path = r'C:\Users\Admin\Downloads\python cleaning fitment\fuzzy_match_MVL.xlsx'

# Output folder
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads\python cleaning fitment")
output_file_path = os.path.join(downloads_folder, "fuzzy_match_OUTPUT.xlsx")

# ====== HELPER FUNCTIONS ======

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = text.replace("(", "").replace(")", "").replace("/", "").replace("-", " ").replace(",", "").strip()
    return text

def create_key(df, source='scraped'):
    if source == 'scraped':
        return (df['Manufacturer'].apply(clean_text) + " " +
                df['Model'].apply(clean_text) + " " +
                df['type'].apply(clean_text))
    else:
        return (df['Make'].apply(clean_text) + " " +
                df['Model'].apply(clean_text) + " " +
                df['Type'].apply(clean_text))

# ====== MAIN WORK ======

# Load the data
print("Loading files...")
scraped_df = pd.read_excel(scraped_file_path)
mvl_df = pd.read_excel(mvl_file_path)

# Create matching keys
scraped_df['match_key'] = create_key(scraped_df, source='scraped')
mvl_df['match_key'] = create_key(mvl_df, source='mvl')

# Matching
print("Matching entries...")
matched_results = []

for idx, row in scraped_df.iterrows():
    search_key = row['match_key']
    match, score, _ = process.extractOne(search_key, mvl_df['match_key'], scorer=fuzz.token_sort_ratio)

    if score >= 85:
        matched_row = mvl_df[mvl_df['match_key'] == match].iloc[0]
        k_type = matched_row['K-Type']
    else:
        k_type = None  # No good match found

    matched_results.append({
        'Manufacturer': row['Manufacturer'],
        'Model': row['Model'],
        'Type': row['type'],
        'Matched K-Type': k_type,
        'Match Score': score
    })

# Create final output DataFrame
output_df = pd.DataFrame(matched_results)

# Save to Downloads folder
output_df.to_excel(output_file_path, index=False)

# Success message
print(f"\n✅ Matching complete! Output saved at: {output_file_path}")