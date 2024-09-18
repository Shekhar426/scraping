import os

path = ["D:\\Google Drive"]

list = []
for path in path:
    l_files = os.listdir(path)
    for file in l_files:
        if file != "$RECYCLE.BIN" and file != "Recovery" and file != "System Volume Information":
            list.append(int(file.replace(".zip", "")))
for i in sorted(list):
    print(i)

