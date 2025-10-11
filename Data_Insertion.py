import mysql.connector
import csv
from mysql.connector import Error

# --- IMPORTANT: CONFIGURATION ---
# 1. Replace these with your actual MySQL database credentials.
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Randula@2006',
    'database': 'filmfestival'
}

# 2. Place all your CSV files in a single folder and update the path below.
#    Replace './path/to/your/csv_files/' with the actual path to that folder.
CSV_BASE_PATH = './dataset_builder/FinalDatasets/'

# Dictionary mapping table names to their corresponding CSV files.
CSV_FILES = {
    'country': 'country_data.csv',
    'genre': 'genre_data.csv',
    'award': 'award_data.csv',
    'person': 'person_data.csv',
    'festival': 'festival_data.csv',
    'film': 'film_data.csv',
    'festival_edition': 'festival_edition_data.csv',
    'film_genre': 'film_genre_data.csv',
    'film_director': 'film_director_data.csv',
    'film_actor': 'film_actor_data.csv',
    'nomination': 'nomination_data.csv'
}

def create_connection():
    # Create a database connection to the MySQL server.
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to the database.")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return connection

def process_row(row):
    
    # Processes a single row from a CSV file.
    # Converts empty strings or 'NULL' strings to Python's None type,
    # so they are inserted SQL as NULL values.
    
    return [None if (value == '' or value.upper() == 'NULL') else value for value in row]

def insert_data(cursor, table_name, columns, file_path, custom_processor=None):
    
    # Generic function to insert data from a CSV file into a database table.

    # Args:
    #     cursor: The database cursor object.
    #     table_name (str): The name of the table to insert data into.
    #     columns (list): A list of column names for the INSERT statement.
    #     file_path (str): The full path to the CSV file.
    #     custom_processor (function, optional): A function to perform special processing on each row.
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row

            data_to_insert = []
            for row in csv_reader:
                if custom_processor:
                    processed_row = custom_processor(row)
                else:
                    processed_row = process_row(row)
                data_to_insert.append(tuple(processed_row))

            if not data_to_insert:
                print(f"No data found in {file_path} for table {table_name}.")
                return

            # Prepare the SQL INSERT statement
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

            # Execute the query
            cursor.executemany(query, data_to_insert)
            print(f"Successfully inserted {cursor.rowcount} rows into the '{table_name}' table.")

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while inserting data into '{table_name}': {e}")


def nomination_processor(row):
    # Custom processor for the Nomination table to handle boolean and NULLs.
    processed = process_row(row)
    # The 'isWinner' column is the 6th element (index 5)
    if processed[5] is not None:
        # Convert 'TRUE'/'FALSE' strings to boolean 1/0 for MySQL
        processed[5] = 1 if str(processed[5]).upper() == 'TRUE' else 0
    return processed


def main():
    # Main function to insert the data into the database in the correct order.
    connection = create_connection()
    if connection is None:
        return

    cursor = None
    try:
        cursor = connection.cursor()

        # The order of insertion is crucial to respect foreign key constraints.
        # Tables without foreign keys are inserted first.
        print("\n--- Starting Data Insertion ---")

        insert_data(cursor, 'Country', ['countryID', 'countryName', 'countryCode'], CSV_BASE_PATH + CSV_FILES['country'])
        insert_data(cursor, 'Genre', ['genreID', 'genreName'], CSV_BASE_PATH + CSV_FILES['genre'])
        insert_data(cursor, 'Award', ['awardID', 'awardName'], CSV_BASE_PATH + CSV_FILES['award'])

        # Tables with dependencies on the above tables
        insert_data(cursor, 'Person', ['personID', 'fullName', 'birthDate', 'countryID'], CSV_BASE_PATH + CSV_FILES['person'])
        insert_data(cursor, 'Festival', ['festivalID', 'festivalName', 'countryID'], CSV_BASE_PATH + CSV_FILES['festival'])
        insert_data(cursor, 'Film', ['filmID', 'title', 'releaseYear', 'duration', 'countryID', 'rating'], CSV_BASE_PATH + CSV_FILES['film'])

        # Tables with more complex dependencies
        insert_data(cursor, 'FestivalEdition', ['editionID', 'festivalID', 'year', 'ceromanyNumber', 'startDate', 'endDate'], CSV_BASE_PATH + CSV_FILES['festival_edition'])
        
        # Junction tables
        insert_data(cursor, 'FilmGenre', ['filmID', 'genreID'], CSV_BASE_PATH + CSV_FILES['film_genre'])
        insert_data(cursor, 'FilmDirector', ['filmID', 'personID'], CSV_BASE_PATH + CSV_FILES['film_director'])
        insert_data(cursor, 'FilmActor', ['filmID', 'personID'], CSV_BASE_PATH + CSV_FILES['film_actor'])
        
        # Final table with the most dependencies, using a custom processor
        insert_data(cursor, 'Nomination', ['nominationID', 'editionID', 'awardID', 'filmID', 'personID', 'isWinner'], CSV_BASE_PATH + CSV_FILES['nomination'], custom_processor=nomination_processor)

        # Commit the changes to the database
        connection.commit()
        print("\n--- All data has been committed to the database successfully! ---")

    except Error as e:
        print(f"A database error occurred: {e}")
        if connection.is_connected():
            connection.rollback()
            print("Transaction rolled back.")
    finally:
        # Clean up the connection and cursor
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")

if __name__ == '__main__':
    main()
