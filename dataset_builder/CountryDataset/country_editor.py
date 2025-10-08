import pandas as pd

# Read the CSV file, selecting only the needed columns
df = pd.read_csv("country code.csv", usecols=["Country", "Alpha-3 code"], encoding="latin1")

# Display the result
print(df)

# Optionally, save to a new CSV file
df.to_csv("countryAndCode.csv", index=False, encoding="utf-8")
