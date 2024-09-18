import os
import glob
import pandas as pd

def json_to_excel(folder_path, output_file):
    # Get a list of all JSON files in the folder
    json_files = glob.glob(os.path.join(folder_path, "*.json"))

    # Create an empty list to store dataframes
    dataframes = []

    # Loop through each JSON file and read it into a DataFrame
    for json_file in json_files:
        df = pd.read_json(json_file)
        dataframes.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Write the combined DataFrame to an Excel file
    combined_df.to_excel(output_file, index=False)

# Example usage
folder_path = "D:\Python\Scraping Projects\Westelm\Dumps_Parsing"  # Replace with your folder path
output_file = "output.xlsx"  # Replace with your desired output Excel file name
json_to_excel(folder_path, output_file)
