import pandas as pd

df = pd.read_json("Data_2.json")
df.to_csv("Data_2.csv", index=True)