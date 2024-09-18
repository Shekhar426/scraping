import pandas as pd

df = pd.read_json("3.json")
df.to_csv('3.csv', index=True)