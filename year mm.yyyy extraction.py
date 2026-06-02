import pandas as pd

# Load your Excel file
input_file = r'C:\Users\Admin\Downloads\to_extract_startyear.xlsx'
output_file = r'C:\Users\Admin\Downloads\to_extract_startyear-output.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(input_file)

# Ensure we use the correct column (e.g., "Title")
date_column = 'Title'  # Adjust based on the exact column name

# Function to extract the earliest start date and latest end date
def extract_start_and_end_dates(date_range):
    if pd.isna(date_range):
        return "", ""  # Return empty if no data
    
    # Split the date range by commas
    date_parts = str(date_range).split(',')
    
    # Initialize a list to hold parsed dates
    parsed_dates = []
    
    for date in date_parts:
        date = date.strip()  # Remove extra whitespace
        if '.' in date:  # Format like MM.YYYY
            parsed_date = pd.to_datetime(date, format='%m.%Y', errors='coerce')
        else:  # Year only format
            parsed_date = pd.to_datetime(date, format='%Y', errors='coerce')
        if not pd.isna(parsed_date):  # Add only valid dates
            parsed_dates.append(parsed_date)
    
    if not parsed_dates:
        return "", ""  # If no valid dates remain, return empty
    
    # Find the earliest and latest dates
    start_date = min(parsed_dates).strftime('%m.%Y')
    end_date = max(parsed_dates).strftime('%m.%Y')
    
    return start_date, end_date

# Apply the function to the correct column
df['Start Month.Year'], df['End Month.Year'] = zip(*df[date_column].apply(extract_start_and_end_dates))

# Save the updated DataFrame to a new Excel file
df.to_excel(output_file, index=False)

print(f"Extracted starting and ending month and year saved to {output_file}")
