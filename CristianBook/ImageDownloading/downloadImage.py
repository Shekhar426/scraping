import openpyxl
import requests
import os

# Load the Excel file
file_path = 'output.xlsx'
print(f"Loading Excel file: {file_path}")
workbook = openpyxl.load_workbook(file_path)
sheet = workbook['Sheet1']

# Create the main folder named 'Image'
main_folder = 'ROGERSPORTS_MIDWAYUSA_08072024'
print(f"Creating main folder: {main_folder}")
os.makedirs(main_folder, exist_ok=True)

# Define file paths for success and failure logs
success_file_path = 'success.txt'
failure_file_path = 'failure.txt'

# Iterate through the rows in the sheet
for row_idx, row in enumerate(sheet.iter_rows(min_row=2, max_col=2, values_only=True), start=2):
    folder_name, cell_value = row
    if cell_value:  # Ensure the cell is not empty
        image_urls = eval(cell_value)  # Convert the string to a list

        # Create a folder named after the folder name in column A inside the 'Image' folder
        folder_path = os.path.join(main_folder, str(folder_name))
        print(f"Downloading images for item: {folder_path}")
        os.makedirs(folder_path, exist_ok=True)

        # Flag to check if all images are downloaded successfully
        all_images_success = True

        # Download each image and save it in the folder
        for idx, url in enumerate(image_urls):
            print(f"Downloading image {idx + 1} from {url}")
            response = requests.get(url)
            if response.status_code == 200:
                image_path = os.path.join(folder_path, f'image_{idx + 1}.jpg')
                with open(image_path, 'wb') as file:
                    file.write(response.content)
            else:
                print(f"Failed to download image {idx + 1} from {url}, status code: {response.status_code}")
                all_images_success = False

        # Record overall success or failure based on the flag
        with open(success_file_path, 'a') as success_file, open(failure_file_path, 'a') as failure_file:
            if all_images_success:
                success_file.write(f"Folder: {folder_name}\n")
                print(f"All images in folder '{folder_name}' have been successfully downloaded and saved.")
            else:
                failure_file.write(f"Folder: {folder_name}\n")
                print(f"One or more images in folder '{folder_name}' failed to download.")

    else:
        print(f"Skipping row {row_idx} as the cell is empty")

print("All images have been processed.")
