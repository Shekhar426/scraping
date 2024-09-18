import json

# Load the JSON file with the correct encoding
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
values_list = list(data.values())

print(type(values_list))
print(len(values_list))

def append_dict_to_list_and_save(dictionary, file_path):
    try:
        # Read the existing data from the JSON file (if it exists)
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, create an empty list
        data = []
    # Append the new dictionary to the list
    data.append(dictionary)
    # Save the updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


for i in values_list:
    print(i)
    append_dict_to_list_and_save(i, 'data3.json')