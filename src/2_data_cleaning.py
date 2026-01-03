import pandas as pd

# Read original Excel file
df = pd.read_excel("data/raw_inflation.xlsx")

# Separate the two title (Turkish and English)
month_TR = df.iloc[0]
month_EN = df.iloc[1]

# Get real data part
df_clean = df.iloc[2:].copy()

# Fix the columns names
columns = ["Year"]  + list(month_EN[1:])
df_clean.columns = columns

#Fix the year(its not an integer)
df_clean["Year"] = df_clean["Year"].astype(int)

print(df_clean.head())
print(df_clean.columns)

# Wide to Long Format
df_long = df_clean.melt(
    id_vars=["Year"],
    var_name="Month",
    value_name="CPI"
)

#Convert month names to the numbers
month_map = {
    "January":1 ,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}
df_long["Number"] = df_long["Month"].map(month_map)

# Make date columns
df_long["Date"] = pd.to_datetime(
    df_long["Year"].astype(str) + "-" + df_long["Number"].astype(str),
    format="%Y-%m"
)

# Delete unnecessary columns and missing CPI values
df_long = df_long.drop(columns=["Month", "Number"])
df_long = df_long.dropna(subset=["CPI"])

# Sort by date
df_long = df_long.sort_values("Date")

# Save the clean data
df_long.to_csv("data/cleaned_inflation.csv", index=False)

print(df_long.head())
print(df_long.tail())
