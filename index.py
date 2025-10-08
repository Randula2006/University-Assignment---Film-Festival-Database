import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="your_database"
)

cursor = conn.cursor()

#countryAndCode.csv
# Read the CSV file, selecting only the needed columns
df = pd.read_csv("countryAndCode.csv", usecols=["Country", "Alpha-3 code"], encoding="utf-8")

# Insert data into the Country table
for index, row in df.iterrows():
    cursor.execute("INSERT INTO Country (countryID, countryName) VALUES (%s, %s)", (row['Alpha-3 code'], row['Country']))


conn.commit()
cursor.close()
conn.close()


