import pandas as pd

df = pd.read_json("Scheels.json")
df.to_csv("Scheels.csv", index=True)