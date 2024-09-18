import pandas as pd

df = pd.read_json("Tractor.json")
df.to_csv('Tractor.csv', index=True)