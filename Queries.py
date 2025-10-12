import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

#load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
#to use the specific database
DB_usage = "USE gunathilake_23610903;"

def Films_and_years():
    #Function to query all the films and their release years from the database

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            query = "SELECT title , releaseYear FROM film;"
            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query)
            results = cursor.fetchall()

            # Determining the maximum length of the film titles for formatting
            if results:
                max_length_title = max(len(row[0]) for row in results) + 2
            else:

                max_length_title = 0#default value if no results

            print("Films and their Release Years:")
            print("==================================================================")
            print("|              Title                              | Release Year |")
            print("==================================================================")
            for row in results:
                print(f"| {row[0]:<{max_length_title}} |     {row[1]}     |")
            print("==================================================================")
        else:
            print("Failed to connect to the database.")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # log
            # print("MySQL connection is closed.")
        
    return