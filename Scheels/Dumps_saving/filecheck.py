import os

def get_file_numbers(folder_path):
    file_numbers = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.html'):
            try:
                number = int(file_name.replace('.html', ''))
                file_numbers.append(number)
            except ValueError:
                print(f"Skipping file with non-integer name: {file_name}")
    return file_numbers

folder_path = 'E:\\dumps_scheels\\No\\'  # Replace with the path to your folder
file_numbers = get_file_numbers(folder_path)

actualPendingList = []
for k in range(1, 28759):
    if k not in file_numbers:
        actualPendingList.append(k)

print(sorted(actualPendingList))
print(len(actualPendingList))