import pandas as pd

# Load the datasets
mvl_file = r"C:\Users\Admin\Downloads\gpt_analysis mvl.xlsx"       # MVL file (contains smaller year ranges)
updated_file = r"C:\Users\Admin\Downloads\gpt_analysis_updated.xlsx"  # Updated file (contains master year ranges)

# Read input data
df_mvl = pd.read_excel(mvl_file)       # MVL
df_updated = pd.read_excel(updated_file) # Updated

# Define the lookup columns (adjust if needed)
mvl_column = "YearRange"        # Column in MVL file
updated_column = "YearRange"    # Column in Updated file

def expand_years(year_range_str):
    """
    Convert '2006-2010' or '2006|2007|2008' into a set of years.
    Handles NaN/empty values safely.
    """
    if pd.isna(year_range_str):   # If empty cell
        return set()
    
    year_range_str = str(year_range_str).strip()
    
    if "-" in year_range_str:     # Case like 2006-2010
        try:
            start, end = map(int, year_range_str.split("-"))
            return set(range(start, end + 1))
        except:
            return set()
    else:                         # Case like 2006|2007|2008
        try:
            return set(map(int, year_range_str.split("|")))
        except:
            return set()

def format_years(years_set):
    """Format a set {2006,2007,2008} → '2006|2007|2008'"""
    return "|".join(str(y) for y in sorted(years_set))

# Expand year ranges in both dataframes
df_mvl["YearSet"] = df_mvl[mvl_column].apply(expand_years)
df_updated["YearSet"] = df_updated[updated_column].apply(expand_years)

# Perform lookup: for each Updated range, collect MVL ranges that are subsets
matched_values = []
for upd_years in df_updated["YearSet"]:
    if not upd_years:  # If no valid years
        matched_values.append("")
        continue
    
    matches = []
    for mvl_years in df_mvl["YearSet"]:
        if mvl_years.issubset(upd_years) and mvl_years:   # MVL is subset of Updated
            matches.append(format_years(mvl_years))
    
    # ✅ Remove duplicates while preserving order
    seen = set()
    unique_matches = []
    for m in matches:
        if m not in seen:
            unique_matches.append(m)
            seen.add(m)
    
    # Join multiple matches with "," as delimiter
    matched_values.append(",".join(unique_matches))

# Add results into Updated file
df_updated["Matched MVL Ranges"] = matched_values

# Save output
output_file = r"C:\Users\Admin\Downloads\vlookup_yearranges_updated_lookup.xlsx"
df_updated.to_excel(output_file, index=False)

print(f"✅ Updated file saved at: {output_file}")
