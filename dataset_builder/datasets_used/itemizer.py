import pandas as pd

df = pd.read_csv("countryAndCode.csv", encoding="latin1")

for _, row in df.iterrows():
    print(f"('{row['Country']}', '{row['Alpha-3 code']}'),")
