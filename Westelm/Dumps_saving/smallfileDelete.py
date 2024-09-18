import os

def delete_small_files(folder_path, size_limit_kb=250):
    # Convert size limit from kilobytes to bytes
    size_limit_bytes = size_limit_kb * 1024
    # Iterate over all the files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Check if it is a filev
        if os.path.isfile(file_path):
            # Get the size of the file
            file_size = os.path.getsize(file_path)
            # If the file size is less than the size limit, delete the file
            if file_size < size_limit_bytes:
                os.remove(file_path)
                print(f"Deleted {file_path} (Size: {file_size} bytes)")

# Example usage
folder_path = 'E:\\dumps_westelm2'
delete_small_files(folder_path)

