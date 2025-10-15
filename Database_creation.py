import mysql.connector
import csv
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- IMPORTANT: CONFIGURATION ---
# 1. Replace these with your actual MySQL database credentials on the .env file
DB_CONFIG = {
    'host': os.getenv('DB_HOST'), 
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# 2. Place all your CSV files in a single folder and update the path below.
# replace it with the file path to the dataset folder
CSV_BASE_PATH = os.getenv('FILE_PATH', './FinalDatasets/')

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

#Main database creation and data insertion functions
def create_connection():
    # Create a database connection to the MySQL server.
    connection = None
    try:
        # ** means dictionary unpacking
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("-Successfully connected to the database to Insert data.")
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

    # Arguments:
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
            # visualize the number of rows inserted
            # print(f"Successfully inserted {cursor.rowcount} rows into the '{table_name}' table.")

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while inserting data into '{table_name}': {e}")

def nomination_processor(row):
    
    # Custom processor for the Nomination table. This function is robust and
    # explicitly converts every column to its correct data type to prevent errors.
  
    # Unpack the row of strings from the CSV file
    nominationID_str, editionID_str, awardID_str, filmID_str, personID_str, isWinner_str = row
    
    
    # Convert all ID columns to integers
    nominationID = int(nominationID_str)
    editionID = int(editionID_str)
    awardID = int(awardID_str)
    filmID = int(filmID_str)
    
    # Explicitly handle the personID, which can be empty or the word 'NULL'
    # If the string is empty OR the word 'NULL', use None, which becomes SQL NULL
    if not personID_str or not personID_str.strip() or personID_str.upper() == 'NULL':
        personID = None
    else:
        # If the string has a number, convert it to an integer
        personID = int(personID_str)
    
    # Explicitly handle the isWinner column
    # Convert the string '1' or '0' into a boolean value (1 or 0)
    isWinner = bool(int(isWinner_str))
    
    # Return the fully processed and correctly typed row as a tuple
    return (nominationID, editionID, awardID, filmID, personID, isWinner)

def create_database(fileName):
    try:
        connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD')
        )
        cursor = connection.cursor()
        print("-connection successful")
        print("-creating database...")

        # read the sql file
        with open(fileName, 'r') as sql_file:
            #read the entire file
            sql_script = sql_file.read()
        
        # splitting the sql script into individual statements
        sql_commands = sql_script.split(';')

        #execute each command one at a time
        for command in sql_commands:
            if command.strip(): # skip empty commands
                cursor.execute(command)

        connection.commit()
        print("-Database created successfully")
        cursor.close()
        connection.close()# close the connection
    
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")

    return

def insert_data_into_db():
    connection = create_connection()
    if connection is None:
        return

    cursor = None
    try:
        cursor = connection.cursor()

        # The order of insertion is crucial to respect foreign key constraints.
        # Tables without foreign keys are inserted first.
        print("\n--Starting Data Insertion")

        insert_data(cursor, 'Country', ['countryID', 'countryName', 'countryCode'], CSV_BASE_PATH + CSV_FILES['country'])
        insert_data(cursor, 'Genre', ['genreID', 'genreName'], CSV_BASE_PATH + CSV_FILES['genre'])
        insert_data(cursor, 'Award', ['awardID', 'awardName'], CSV_BASE_PATH + CSV_FILES['award'])

        # Tables with dependencies on the above tables
        insert_data(cursor, 'Person', ['personID', 'fullName', 'birthDate', 'countryID'], CSV_BASE_PATH + CSV_FILES['person'])
        insert_data(cursor, 'Festival', ['festivalID', 'festivalName', 'countryID'], CSV_BASE_PATH + CSV_FILES['festival'])
        insert_data(cursor, 'Film', ['filmID', 'title', 'releaseYear', 'duration', 'countryID', 'rating'], CSV_BASE_PATH + CSV_FILES['film'])

        # Tables with more complex dependencies
        # FIX: Corrected typo from 'ceromanyNumber' to 'ceremonyNumber'
        insert_data(cursor, 'FestivalEdition', ['editionID', 'festivalID', 'year', 'ceremonyNumber', 'startDate', 'endDate'], CSV_BASE_PATH + CSV_FILES['festival_edition'])
        
        # Junction tables
        insert_data(cursor, 'FilmGenre', ['filmID', 'genreID'], CSV_BASE_PATH + CSV_FILES['film_genre'])
        insert_data(cursor, 'FilmDirector', ['filmID', 'personID'], CSV_BASE_PATH + CSV_FILES['film_director'])
        insert_data(cursor, 'FilmActor', ['filmID', 'personID'], CSV_BASE_PATH + CSV_FILES['film_actor'])
        
        # Final table with the most dependencies, using a custom processor
        insert_data(cursor, 'Nomination', ['nominationID', 'editionID', 'awardID', 'filmID', 'personID', 'isWinner'], CSV_BASE_PATH + CSV_FILES['nomination'], custom_processor=nomination_processor)

        # Commit the changes to the database
        connection.commit()
        print("-All data has been inserted to the database successfully!")

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
            print("-MySQL connection is closed.\n")
    return

def run_sql_command(command, success_message):
    # Helper function to connect, run a single command, commit, and close.
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            # The python connector does not support the DELIMITER command.
            # We must execute each statement separately.
            # For complex triggers/procedures, we pass the whole block at once.
            cursor.execute(command)
            connection.commit()
            print(success_message)
    except Error as e:
        print(f"Error executing command: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()

#Indexes
def create_indexes():
    #Function to create indexes on the database tables.
    run_sql_command("CREATE INDEX idx_film_title ON Film(title);", "-Index on Film(title) created.")
    run_sql_command("CREATE INDEX idx_person_fullName ON Person(fullName);", "-Index on Person(fullName) created.\n")


#Views
def create_view_AllWinners():
    # Function to create a SQL view in the database.
    run_sql_command("DROP VIEW IF EXISTS AllWinners;", "-Dropped existing view AllWinners if it exists.")
    view_query = """
    CREATE VIEW AllWinners AS
    SELECT f.title, p.fullName AS Person_FullName, a.awardName, fe.festivalName, feE.year
    FROM nomination AS n
    INNER JOIN film AS f ON n.filmID = f.filmID
    INNER JOIN person AS p ON n.personID = p.personID
    INNER JOIN award AS a ON n.awardID = a.awardID
    INNER JOIN festivalEdition AS feE ON n.editionID = feE.editionID
    INNER JOIN festival AS fe ON feE.festivalID = fe.festivalID
    WHERE n.isWinner = TRUE;
    """
    run_sql_command(view_query, "-View 'AllWinners' created successfully.\n")

def create_view_FilmSummary():
    #Function to create a SQL view in the database.
    run_sql_command("DROP VIEW IF EXISTS FilmSummary;", "-Dropped existing view FilmSummary if it exists.")
    view_query = """
    CREATE VIEW FilmSummary AS
    SELECT f.title as FilmTitle, 
           COUNT(n.nominationID) AS TotalNominations, 
           COUNT(CASE WHEN n.isWinner = TRUE THEN 1 END) AS TotalWins
    FROM film AS f LEFT JOIN nomination AS n ON f.filmID = n.filmID
    GROUP BY f.filmID, f.title;
    """
    run_sql_command(view_query, "-View 'FilmSummary' created successfully.\n")


# Triggers
def alter_film_table():
    #Function to alter the Film table to add a new column 'rating'.
    try:
        run_sql_command(
            "ALTER TABLE film ADD COLUMN nomination_count INT NOT NULL DEFAULT 0;",
            "-Column 'nomination_count' added to 'Film' table successfully.\n"
        )
    except Error as e:
        # Catch specific error if column already exists and print a friendlier message
        if e.errno == 1060: # Error code for 'Duplicate column name'
            print("-Column 'nomination_count' already exists in 'Film' table.")
        else:
            print(f"Error altering table: {e}")

def Trigger_after_nomination_insert():
    #Function to create a trigger that updates the nomination_count in the Film table after a new nomination is inserted.
    run_sql_command("DROP TRIGGER IF EXISTS after_nomination_insert;", "-Dropped trigger 'after_nomination_insert' if it exists.")
    trigger_query = """
    CREATE TRIGGER after_nomination_insert
    AFTER INSERT ON nomination
    FOR EACH ROW
    BEGIN
        UPDATE film
        SET nomination_count = nomination_count + 1
        WHERE filmID = NEW.filmID;
    END
    """
    run_sql_command(trigger_query, "-Trigger 'after_nomination_insert' created successfully.\n")

def Trigger_prevent_winner_deletion():
    #Function to create a trigger that prevents deletion of nominations marked as winners.
    run_sql_command("DROP TRIGGER IF EXISTS prevent_winner_deletion;", "-Dropped trigger 'prevent_winner_deletion' if it exists.")
    trigger_query = """
    CREATE TRIGGER prevent_winner_deletion
    BEFORE DELETE ON nomination
    FOR EACH ROW
    BEGIN
        -- old refers to the row that about to be deleted
        -- we check the isWinner column of that row
        IF OLD.isWinner = TRUE THEN
            -- if the nomination is a winner, we raise an error to prevent deletion
            -- we set a custom error message to inform the user about the reason
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot delete a nomination that is marked as a winner.';
        END IF;
    END
    """
    run_sql_command(trigger_query, "-Trigger 'prevent_winner_deletion' created successfully.\n")


#procedures
def procedure_getPersonAwardHistory():
    run_sql_command("DROP PROCEDURE IF EXISTS GetPersonAwardHistory;", "-Dropped procedure 'GetPersonAwardHistory' if it exists.")
    proc_query = """
    CREATE PROCEDURE GetPersonAwardHistory(IN person_name VARCHAR(100))
    BEGIN
        SELECT 
            f.title AS FilmTitle,
            a.awardName AS AwardName,
            fe.festivalName AS FestivalName,
            feE.year AS EditionYear,
            CASE
                WHEN n.isWinner = TRUE THEN 'Winner'
                ELSE 'Nominee'
            END AS Status
        FROM person AS p
        JOIN nomination AS n ON p.personID = n.personID
        JOIN film AS f ON n.filmID = f.filmID
        JOIN award AS a ON n.awardID = a.awardID
        JOIN festivalEdition AS feE ON n.editionID = feE.editionID
        JOIN festival AS fe ON feE.festivalID = fe.festivalID
        WHERE p.fullName = person_name
        ORDER BY feE.year DESC;
    END
    """
    run_sql_command(proc_query, "-Procedure 'GetPersonAwardHistory' created successfully.\n")

def procedure_updateWinnerStatus():
    run_sql_command("DROP PROCEDURE IF EXISTS UpdateWinnerStatus;", "-Dropped procedure 'UpdateWinnerStatus' if it exists.")
    proc_query = """
    CREATE PROCEDURE UpdateWinnerStatus(
        IN in_filmTitle VARCHAR(255), 
        IN in_awardName VARCHAR(100), 
        IN in_festivalName VARCHAR(100),
        IN in_editionYear INT, 
        IN in_personName VARCHAR(100), 
        IN new_winner_status BOOLEAN,
        OUT out_message VARCHAR(255)
    )
    BEGIN
        -- Declare variables to hold IDs found from the input parameters
        DECLARE v_nominationID, v_rowCount INT;

        -- Find the nominationID based on the provided details

        SELECT n.nominationID INTO v_nominationID
        FROM nomination AS n
            JOIN film AS f ON n.filmID = f.filmID
            JOIN award AS a ON n.awardID = a.awardID
            JOIN festivalEdition AS feE ON n.editionID = feE.editionID
            JOIN festival AS fe ON feE.festivalID = fe.festivalID
            LEFT JOIN person AS p ON n.personID = p.personID

        WHERE 
            f.title = in_filmTitle 
            AND a.awardName = in_awardName 
            AND fe.festivalName = in_festivalName
            AND feE.year = in_editionYear 
            AND (
                    in_personName IS NULL 
                    OR p.fullName = in_personName
            )
        LIMIT 1;

        -- if matching nomination is found, update its winner status

        IF v_nominationID IS NOT NULL THEN

            UPDATE nomination 
                SET isWinner = new_winner_status 
                WHERE  
                    nominationID = v_nominationID;
            SELECT ROW_COUNT() INTO v_rowCount;
            
            IF v_rowCount > 0 THEN 
                SET out_message = 'Nomination winner status updated successfully.';
            ELSE 
                SET out_message = 'No changes made to the nomination winner status.'; 
            END IF;

        ELSE 
            SET out_message = 'No matching nomination found with the provided details.'; 
        END IF;

    END
    """
    run_sql_command(proc_query, "-Procedure 'UpdateWinnerStatus' created successfully.\n")

def procedure_deleteFestivalEdition():
    run_sql_command("DROP PROCEDURE IF EXISTS DeleteFestivalEdition;", "-Dropped procedure 'DeleteFestivalEdition' if it exists.")
    
    proc_query = """
    CREATE PROCEDURE DeleteFestivalEdition(
        IN in_festivalName VARCHAR(100), 
        IN in_editionYear INT,
        OUT out_message VARCHAR(255)
    )
    BEGIN
        -- Declare Variables
        DECLARE v_editionID, v_rowCount INT;

        -- Find the editionID based on the provided festival name and year

        SELECT feE.editionID INTO v_editionID
            FROM festivalEdition AS feE
                JOIN festival AS fe ON feE.festivalID = fe.festivalID
            WHERE fe.festivalName = in_festivalName AND feE.year = in_editionYear
        LIMIT 1;

        -- If the edition is found, proceed to delete

        IF v_editionID IS NOT NULL THEN
            DELETE FROM festivalEdition 
            WHERE editionID = v_editionID;

            -- check row count to see if a row was actually deleted

            SELECT ROW_COUNT() INTO v_rowCount;
                IF v_rowCount > 0 THEN 
                    SET out_message = CONCAT('Festival edition ', in_festivalName, ' ', in_editionYear, ' deleted successfully.');
                ELSE 
                    SET out_message = 'No festival edition was deleted.'; 
                END IF;

        ELSE 
            SET out_message = 'No matching festival edition found with the provided details.'; 
        END IF;
    END
    """
    run_sql_command(proc_query, "-Procedure 'DeleteFestivalEdition' created successfully.\n")


# Made by Randula Gunathilake