import pandas as pd

df = pd.read_json("opticsplanet.json")
df.to_csv("opticsplanet.csv", index=True)