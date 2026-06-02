# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 19:47:48 2025

@author: Admin
"""

import pandas as pd

# Load the Excel file
file_path = r'C:\Users\Admin\Downloads\HTML line breaker remove output.xlsx'  # Update with actual path
df = pd.read_excel(file_path)

# Forward fill only Column B (assuming it's the second column)
df.iloc[:, 4] = df.iloc[:, 4].ffill()

# Save the cleaned file
output_path = r'C:\Users\Admin\Downloads\HTML line breaker remove.xlsx'
df.to_excel(output_path, index=False)

print("Column B has been forward filled successfully.")
