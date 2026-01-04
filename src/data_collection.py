"""
This module is responsible for loading raw inflation data from the source file.
It reads the original Excel dataset and performs initial inspection by printing
basic information such as the first rows, column names, and dataset shape.
"""

import pandas as pd

df = pd.read_excel("data/raw_inflation.xlsx")

print(df.head())
print(df.columns)
print(df.shape)
