import pandas as pd

df = pd.read_excel("data/raw_inflation.xlsx")

print(df.head())
print(df.columns)
print(df.shape)