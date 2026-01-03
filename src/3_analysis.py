import pandas as pd
import numpy as np
from scipy import stats

try:
    df = pd.read_csv("data/cleaned_inflation.csv")
    print(df.head())
except FileNotFoundError:
    print("ERROR: cleaned_inflation.csv not found in data/ directory.")
    raise
except Exception as e:
    print("ERROR while loading cleaned data:", e)
    raise

print("\n=== Data Loaded Successfully ===")
print(f"Number of records: {len(df)}")
print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")

print("\n=== Running Baseline Statistics ===")
 #Baseline statistic
main_cpi = df["CPI"].mean()
min_cpi = df["CPI"].min()
max_cpi = df["CPI"].max()
sum_cpi = df["CPI"].sum()

print("\n---  Basic Statistic ---")
print("Mean CPI:", main_cpi)
print("Min CPI:", min_cpi)
print("Max CPI:", max_cpi)
print("Sum CPI:", sum_cpi)


 #Advanced statistic
Q1 = df["CPI"].quantile(0.25)
Q2 = df["CPI"].quantile(0.50)
Q3 = df["CPI"].quantile(0.75)
IQR = Q3 - Q1

print("\n--- Quartiles ---")
print("Q1 (%25):", Q1)
print("Q2 (%50):", Q2)
print("Q3 (%75):", Q3)
print("IQR ", IQR)

print("\n=== Running Advanced Statistics (Quartiles & IQR) ===")

# Z-score calculation safety check
if "CPI" not in df.columns:
    raise ValueError("CPI column not found in dataset.")
df["z_score"] = stats.zscore(df["CPI"])

#Threshold for anomaly detection
threshold = 3
anomalies = df[np.abs(df["z_score"]) > threshold]
print("\n---  Anomaly Detection ---")
print("Number of anomalies:", len(anomalies))
print(anomalies[["Date", "CPI", "z_score"]])

print("Anomalies saved to data/anomalies.csv")

#save anomalies for report
try:
    anomalies.to_csv("data/anomalies.csv", index=False)
except Exception as e:
    print("ERROR while saving anomalies.csv:", e)
    raise

print("\n--- Anomalies Analysis Complete Successfully ! ---")

 #Yearly Average CPI
if "Year" not in df.columns:
    raise ValueError("Year column not found in dataset.")
yearly_avg =(
    df.groupby("Year")["CPI"]
    .mean()
    .reset_index()
    .sort_values("Year")
)

print("\n=== Computing Yearly Average CPI ===")

#Year-over-Year Inflation increase(%)
yearly_avg["InflationIncrease"] = yearly_avg["CPI"].pct_change() * 100
yearly_avg["InflationIncrease"] = yearly_avg["InflationIncrease"].fillna(0)

print("\n--- Yearly Inflation Increase --- ")
print(yearly_avg.head())

 #Save analysis
try:
    yearly_avg.to_csv("data/yearly_inflation_increase.csv", index=False)
except Exception as e:
    print("ERROR while saving yearly_inflation_increase.csv:", e)
    raise
print("Yearly inflation analysis saved to data/yearly_inflation_increase.csv")

print("\n--- Yearly Inflation Analysis Complete Successfully ! ---")

# === React-safe CSV ===
react_df = yearly_avg[["Year", "InflationIncrease"]].copy()

# Ensure numeric and dot decimal
react_df["InflationIncrease"] = react_df["InflationIncrease"].astype(float)
react_df["Year"] = react_df["Year"].astype(int)

react_df.to_csv(
    "data/yearly_inflation_increase_react.csv",
    index=False,
    float_format="%.2f"
)

print("React-safe CSV generated.")