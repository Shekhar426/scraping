import os

def list_folders(main_folder_path):
    try:
        # Get the list of all files and directories in the specified path
        items = os.listdir(main_folder_path)

        # Filter out only the directories
        folders = [item for item in items if os.path.isdir(os.path.join(main_folder_path, item))]

        # Print the list of folders
        print("Folders inside '{}':".format(main_folder_path))

        folderList = []
        for folder in folders:
            folderList.append(int(folder))
        print(sorted(folderList))
        print(len(folderList))
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
main_folder_path = "E:\dumps_rh/"
list_folders(main_folder_path)
