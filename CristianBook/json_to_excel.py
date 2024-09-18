import os
import pandas as pd
import json
import openpyxl
from openpyxl.utils.exceptions import IllegalCharacterError

def clean_data(value):
    # Replace or remove illegal characters
    if isinstance(value, str):
        return ''.join(char if char.isprintable() else '' for char in value)
    return value

def json_to_excel(folder_path, output_excel):
    all_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

                if isinstance(json_data, list):
                    df = pd.DataFrame(json_data)
                else:
                    df = pd.DataFrame([json_data])

                # Clean the DataFrame by applying the clean_data function
                df = df.applymap(clean_data)

                all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)

    # Try writing the DataFrame to Excel and catch IllegalCharacterError
    try:
        combined_df.to_excel(output_excel, index=False)
    except IllegalCharacterError as e:
        print(f"Error writing to Excel: {e}")

# Usage example
folder_path = 'D:\\Scraping Projects\\CristianBook\\description'
output_excel = 'output.xlsx'
json_to_excel(folder_path, output_excel)
