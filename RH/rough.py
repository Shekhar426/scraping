for i in range(1, 40):
    print(f"docker run -d -v E:\json_rh:/usr/src/app/json_rh rh --start {i} --end {i+1}")