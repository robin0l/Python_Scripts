import pandas as pd

# Load the datasets
d1 = pd.read_excel(r"C:\Users\admin\Downloads\input python anshu.xlsx")
d2 = pd.read_excel(r"C:\Users\admin\Downloads\Mvl python anshu.xlsx")

# Create dictionaries to store matches
make_model_matches = {}
make_year_matches = {}
make_model_year_matches = {}
make_model_submodel_matches = {}       # New dictionary for Make, Model, and Submodel combination
make_model_submodel_year_matches = {}  

# Iterate through rows in d2 and populate the match dictionaries
for index, row in d2.iterrows():
    make = row["Make"]
    model = row["Models"]
    year = row["Year"]
    submodel = row["Submodel"]

    # Check for Make, Model, Submodel, and Year combination
    if pd.notna(make) and pd.notna(model) and pd.notna(submodel) and pd.notna(year):
        key = (make, model, submodel, year)
        if key not in make_model_submodel_year_matches:
            make_model_submodel_year_matches[key] = []
        make_model_submodel_year_matches[key].append(row)

    # Check for Make, Model, and Year combination
    if pd.notna(make) and pd.notna(model) and pd.notna(year):
        key = (make, model, year)
        if key not in make_model_year_matches:
            make_model_year_matches[key] = []
        make_model_year_matches[key].append(row)

    # Check for Make, Model, and Submodel combination
    if pd.notna(make) and pd.notna(model) and pd.notna(submodel):
        key = (make, model, submodel)
        if key not in make_model_submodel_matches:
            make_model_submodel_matches[key] = []
        make_model_submodel_matches[key].append(row)

    # Check for Make and Model combination
    if pd.notna(make) and pd.notna(model):
        key = (make, model)
        if key not in make_model_matches:
            make_model_matches[key] = []
        make_model_matches[key].append(row)

    # Check for Make and Year combination
    if pd.notna(make) and pd.notna(year):
        key = (make, year)
        if key not in make_year_matches:
            make_year_matches[key] = []
        make_year_matches[key].append(row)

# Function to find ePIDs for Make, Model, Submodel, and Year combination
def find_epids_submodel_year(make, model, submodel, year):
    ePIDs = []
    key = (make, model, submodel, year)
    if key in make_model_submodel_year_matches:
        matches = make_model_submodel_year_matches[key]
        ePIDs.extend([str(match_row["K-Type"]) for match_row in matches])
    return ePIDs

# Function to find ePIDs for Make, Model, and Year combination
def find_epids_model_year(make, model, year, submodel):
    ePIDs = []
    key = (make, model, year)
    if key in make_model_year_matches:
        matches = make_model_year_matches[key]
        for match_row in matches:
            if pd.isna(submodel) or match_row["Submodel"] == submodel:
                ePIDs.extend(str(match_row["K-Type"]).split(','))
    return ePIDs

# Function to find ePIDs for Make, Model, and Submodel combination
def find_epids_model_submodel(make, model, submodel, year):
    ePIDs = []
    key = (make, model, submodel)
    if key in make_model_submodel_matches:
        matches = make_model_submodel_matches[key]
        for match_row in matches:
            if pd.isna(year) or match_row["Year"] == year:
                ePIDs.extend(str(match_row["K-Type"]).split(','))
    return ePIDs

# Function to find ePIDs for Make and Model combination
def find_epids_model(make, model, submodel, year):
    ePIDs = []
    key = (make, model)
    if key in make_model_matches:
        matches = make_model_matches[key]
        for match_row in matches:
            if (pd.isna(submodel) or match_row["Submodel"] == submodel) and (pd.isna(year) or match_row["Year"] == year):
                ePIDs.extend(str(match_row["K-Type"]).split(','))
    return ePIDs

# Function to find ePIDs for Make and Year combination
#def find_epids_year(make, year, model, submodel):
#   ePIDs = []
#  key = (make, year)
#    if key in make_year_matches:
#        matches = make_year_matches[key]
#        for match_row in matches:
#            if pd.isna(model) or match_row["Models"] == model:
#                ePIDs.extend(str(match_row["K-Type"]).split(','))
#    return ePIDs

# Apply the functions to each row in d1 to get and assign the ePIDs
def assign_epids(row):
    make = row["Make"]
    model = row["Models"]
    submodel = row["Submodel"]
    year = row["Year"]

    if pd.notna(make):
        ePIDs = []

        if pd.notna(model) and pd.notna(submodel) and pd.notna(year):
            ePIDs.extend(find_epids_submodel_year(make, model, submodel, year))
        elif pd.notna(model) and pd.notna(year):
            ePIDs.extend(find_epids_model_year(make, model, year, submodel))
        elif pd.notna(model) and pd.notna(submodel):
            ePIDs.extend(find_epids_model_submodel(make, model, submodel, year))
        elif pd.notna(model):
            ePIDs.extend(find_epids_model(make, model, submodel, year))
        elif pd.notna(year):
            ePIDs.extend(find_epids_year(make, year, model, submodel))

        return ', '.join(ePIDs) if ePIDs else ""

# Apply the function to each row in d1 to get and assign the ePIDs
d1["ePIDs"] = d1.apply(assign_epids, axis=1)

# Write the updated d1 data frame to a new Excel file
d1.to_excel(r'C:\Users\admin\Downloads\input python anshu out.xlsx', index=False)
