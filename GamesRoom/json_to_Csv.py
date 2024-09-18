import pandas as pd

df = pd.read_json("gameroom.json")
df.to_csv("gameroom.csv", index=True)

