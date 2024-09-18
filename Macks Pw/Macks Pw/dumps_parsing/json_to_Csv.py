import pandas as pd

df = pd.read_json("Data_1.json")
df.to_csv("Data_1.csv", index=True)