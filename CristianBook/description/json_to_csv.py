import pandas as pd

def convert_json_to_csv(json_files, output_csv):
    # List to hold dataframes
    df_list = []

    # Loop through each json file and read it into a dataframe
    for json_file in json_files:
        df = pd.read_json(json_file)
        df_list.append(df)

    # Concatenate all dataframes into a single dataframe
    combined_df = pd.concat(df_list, ignore_index=True)

    # Save the combined dataframe to a CSV file
    combined_df.to_csv(output_csv, index=False)


filename = "6"
# Example usage
json_files = [f"{filename}.json"]  # List your JSON files here
output_csv = f"{filename}.csv"
convert_json_to_csv(json_files, output_csv)
