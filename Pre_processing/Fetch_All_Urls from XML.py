import csv

# Open the input CSV file
input_file_path = '../Topo Centras/Technorama/urls.csv'

with open(input_file_path, 'r') as input_csv_file:
    # Create a CSV reader
    csv_reader = csv.reader(input_csv_file)

    # Extract URLs from each row
    urls = [row[0] for row in csv_reader]

# Open or create the output CSV file
output_file_path = 'output_urlsNP.csv'
with open(output_file_path, 'w', newline='') as output_csv_file:
    # Create a CSV writer
    csv_writer = csv.writer(output_csv_file)

    # Write the URLs to the new CSV file
    for url in urls:
        if "/p/" not in url:
            csv_writer.writerow([url])
print(f"URLs have been written to {output_file_path}")
