import mysql.connector
import csv
from mysql.connector import Error
import os
from dotenv import load_dotenv
import Menu

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
        connection = mysql.connector.connect(**DB_CONFIG)#** means dictionary unpacking
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
    # Custom processor for the Nomination table to handle boolean and NULLs.
    processed = process_row(row)
    # The 'isWinner' column is the 6th element (index 5)
    if processed[5] is not None:
        # Convert 'TRUE'/'FALSE' strings to boolean 1/0 for MySQL
        processed[5] = 1 if str(processed[5]).upper() == 'TRUE' else 0
    return processed

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
        insert_data(cursor, 'FestivalEdition', ['editionID', 'festivalID', 'year', 'ceromanyNumber', 'startDate', 'endDate'], CSV_BASE_PATH + CSV_FILES['festival_edition'])
        
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


#Indexes
def create_indexes():
    #Function to create indexes on the database tables.
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()

            # Use the specific database
            DB_usage = f"USE {DB_CONFIG['database']};"
            cursor.execute(DB_usage)

            # Define the SQL for creating indexes
            index1 = "CREATE INDEX idx_film_title ON film(title);"
            index2 = "CREATE INDEX idx_person_fullName ON person(fullName);"

            cursor.execute(index1)
            cursor.execute(index2)
            connection.commit()
            print("-Indexes created successfully.")
            cursor.close()
            connection.close() # close the connection
    except Error as e:
        print(f"Error creating indexes: {e}")


#Views
def create_view_AllWinners():
    # Function to create a SQL view in the database.
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            # Use the specific database
            DB_usage = f"USE {DB_CONFIG['database']};"
            cursor.execute(DB_usage)

            # Drop the view if it already exists
            delete_query = "DROP VIEW IF EXISTS AllWinners;"
            cursor.execute(delete_query)

            # Define the SQL for creating the view
            query = """
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
        
            cursor.execute(query)
            connection.commit()
            print("-View 'AllWinners' created successfully.")
            cursor.close()
            connection.close() # close the connection
    except Error as e:
        print(f"Error creating view: {e}")

def create_view_FilmSummary():
    #Function to create a SQL view in the database.

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            # Use the specific database
            DB_usage = f"USE {DB_CONFIG['database']};"
            cursor.execute(DB_usage)
            # Drop the view if it already exists
            delete_query = "DROP VIEW IF EXISTS FilmSummary;"
            cursor.execute(delete_query)

            # Define the SQL for creating the view
            # This view provides a summary of films with their genres, directors, and actors.
            query = """
                    CREATE VIEW FilmSummary AS
                    SELECT f.title as FilmTitle, COUNT(n.nominationID) AS TotalNominations, COUNT(CASE WHEN n.isWinner = TRUE THEN 1 END) AS TotalWins
                    FROM film AS f LEFT JOIN nomination AS n ON f.filmID = n.filmID
                    GROUP BY f.filmID;
                    """
            cursor.execute(query)
            connection.commit()
            print("-View 'FilmSummary' created successfully.")
            cursor.close()
            connection.close() # close the connection
    except Error as e:
        print(f"Error creating view: {e}")


# Triggers
def alter_film_table():
    #Function to alter the Film table to add a new column 'rating'.
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            # Use the specific database
            DB_usage = f"USE {DB_CONFIG['database']};"
            cursor.execute(DB_usage)

            # Define the SQL for altering the table
            query = "ALTER TABLE film ADD COLUMN nomination_count INT NOT NULL DEFAULT 0;"

            cursor.execute(query)
            connection.commit()
            print("-Column 'rating' added to 'Film' table successfully.")
            cursor.close()
            connection.close() # close the connection
        
    except Error as e:
        print(f"Error altering table: {e}")

def Trigger_after_nomination_insert():
    #Function to create a trigger that updates the nomination_count in the Film table after a new nomination is inserted.
    
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            # Use the specific database
            DB_usage = f"USE {DB_CONFIG['database']};"
            cursor.execute(DB_usage)

            # Drop the trigger if it already exists
            delete_query = "DROP TRIGGER IF EXISTS update_nomination_count;"
            cursor.execute(delete_query)

            # Define the SQL for creating the trigger
            query = """
                    DELIMITER $$
                    CREATE TRIGGER after_nomination_insert
                    AFTER INSERT ON nomination
                    FOR EACH ROW
                    BEGIN
                        UPDATE film
                        SET nomination_count = nomination_count + 1
                        WHERE filmID = NEW.filmID;
                    END;
                        $$
                    DELIMITER ;
                    """

            cursor.execute(query)
            connection.commit()
            print("-Trigger 'after_nomination_insert' created successfully.")
            cursor.close()
            connection.close() # close the connection
        
    except Error as e:
        print(f"Error creating trigger: {e}")

def Trigger_prevent_winner_deletion():
    #Function to create a trigger that prevents deletion of nominations marked as winners.
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            # Use the specific database
            DB_usage = f"USE {DB_CONFIG['database']};"
            cursor.execute(DB_usage)

            # Drop the trigger if it already exists
            delete_query = "DROP TRIGGER IF EXISTS prevent_winner_deletion;"
            cursor.execute(delete_query)

            # Define the SQL for creating the trigger
            query = """
                    DELIMITER $$
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
                    END;
                    $$
                    DELIMITER ;
                    """

            cursor.execute(query)
            connection.commit()
            print("-Trigger 'prevent_winner_deletion' created successfully.")
            cursor.close()
            connection.close() # close the connection
        
    except Error as e:
        print(f"Error creating trigger: {e}")


#procedures
def procedure_getPersonAwardHistory():
    connection = mysql.connector.connect(**DB_CONFIG)

    try:
        if connection.is_connected():
            
            cursor = connection.cursor()

            # Use the specific database
            DB_usage = f"USE {DB_CONFIG['database']};"
            cursor.execute(DB_usage)
            # Drop the procedure if it already exists
            delete_query = "DROP PROCEDURE IF EXISTS GetPersonAwardHistory;"
            cursor.execute(delete_query)

            # Define the SQL for creating the procedure
            query = """
                    DELIMITER $$
                    CREATE PROCEDURE GetPersonAwardHistory(
                        IN person_name VARCHAR(100)
                    )

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

                    END $$
                    DELIMITER ;
                    """
            
            cursor.execute(query)
            connection.commit()
            print("-Procedure 'GetPersonAwardHistory' created successfully.")
            cursor.close()
            connection.close() # close the connection
    except Error as e:
        print(f"Error creating procedure: {e}")

#Citation:-
# Title :- Creating a Stored Procedure with Multiple Inserts and Conditional Logic in MySQL
# Author :- Gemini Pro
# Date :- 2025/10/12
def procedure_InsertFullNomination():
    connection = mysql.connector.connect(**DB_CONFIG)

    try:
        if connection.is_connected():
            cursor = connection.cursor()

            # Use the specific database
            DB_usage = f"USE {DB_CONFIG['database']};"
            cursor.execute(DB_usage)

            # Drop the procedure if it already exists
            delete_query = "DROP PROCEDURE IF EXISTS InsertFullNomination;"
            cursor.execute(delete_query)

            # Define the SQL for creating the procedure
            query = """
                    DELIMITER $$
                    CREATE PROCEDURE InsetFullNomination(
                        -- Film details
                        IN in_filmTitle VARCHAR(255),
                        IN in_releaseYear INT,
                        In in_duration INT,

                        -- Person details (can be null for film only awards)
                        IN in_personName VARCHAR(100),
                        IN in_birthDate DATE,
                        IN in_personCountry VARCHAR(100),
                        In in_personCountryCode VARCHAR(3),

                        -- Award festival and edition details
                        IN in_awardName VARCHAR(100),
                        IN in_festivalName VARCHAR(100),
                        In in_festivalCountry VARCHAR(100),
                        In in_festivalCountryCode VARCHAR(3),
                        IN in_editionYear INT,
                        IN in_EditionCeromanyNumber INT,
                        In in_editionStartDate DATE,
                        In in_editionEndDate DATE,

                        -- Nomination details
                        In is_winner BOOLEAN,

                        -- output a message to indicate success or failure
                        OUT out_message VARCHAR(255)
                    )  

                    BEGIN
                        -- declare variable to hold the foreign keys needed for the nomination table
                        DECLARE v_filmID INT;
                        DECLARE v_personID INT;
                        DECLARE v_awardID INT;
                        DECLARE v_editionID INT;
                        DECLARE v_festivalID INT;
                        DECLARE v_personCountryID INT;
                        DECLARE v_festivalCountryID INT;


                        -- check if the film is already in the film table
                        SELECT filmID INTO v_filmID FROM film WHERE title = in_filmTitle LIMIT 1;

                        -- if not found insert the film , (v_filmID will be null)
                        IF v_filmID IS NULL THEN
                            INSERT INTO film (title, releaseYear, duration) 
                            VALUES (in_filmTitle, in_releaseYear, in_duration);
                            SET v_filmID = LAST_INSERT_ID();
                        END IF;

                        -- check if the person is already in the person table (if noly the name is provided)
                        IF in_personName IS NOT NULL AND in_personName != '' THEN
                            SELECT countryID INTO v_personCountryID FROM country WHERE countryName = in_personCountry LIMIT 1;

                            IF v_personCountryID IS NULL AND in_personCountry IS NOT NULL AND in_personCountry != '' THEN
                                INSERT INTO country (countryName, countryCode)
                                VALUES (in_personCountry, in_personCountryCode);
                                SET v_personCountryID = LAST_INSERT_ID();
                            END IF;

                            SELECT personID INTO v_personID FROM person WHERE fullName = in_personName LIMIT 1;
                            IF v_personID IS NULL THEN
                                INSERT INTO person (fullName, birthDate, countryID)
                                VALUES (in_personName, in_birthDate, v_personCountryID);
                                SET v_personID = LAST_INSERT_ID();
                            END IF;
                        ELSE
                            SET v_personID = NULL; -- No person involved in this nomination
                        END IF;

                        -- Find and create the award
                        SELECT awardID INTO v_awardID FROM award WHERE awardName = in_awardName LIMIT 1;
                        IF v_awardID IS NULL THEN
                            INSERT INTO award (awardName) VALUES (in_awardName);
                            SET v_awardID = LAST_INSERT_ID();
                        END IF;

                        -- Find and create the festival and its country
                        SELECT countryID INTO v_festivalCountryID FROM country WHERE countryName = in_festivalCountry LIMIT 1;
                        IF v_festivalCountryID IS NULL THEN
                            INSERT INTO country (countryName, countryCode)
                            VALUES (in_festivalCountry, in_festivalCountryCode);
                            SET v_festivalCountryID = LAST_INSERT_ID();
                        END IF;

                        -- Find or create the festival
                        SELECT festivalID INTO v_festivalID FROM festival WHERE festivalName = in_festivalName LIMIT 1;
                        IF v_festivalID IS NULL THEN
                            INSERT INTO festival (festivalName, countryID)
                            VALUES (in_festivalName, v_festivalCountryID);
                            SET v_festivalID = LAST_INSERT_ID();
                        END IF;

                        -- Find or create the festival edition
                        SELECT editionID INTO v_editionID FROM festivalEdition 
                        WHERE festivalID = v_festivalID AND year = in_editionYear LIMIT 1;
                        IF v_editionID IS NULL THEN
                            INSERT INTO festivalEdition (festivalID, year, ceromanyNumber, startDate, endDate)
                            VALUES (v_festivalID, in_editionYear, in_EditionCeromanyNumber, in_editionStartDate, in_editionEndDate);
                            SET v_editionID = LAST_INSERT_ID();
                        END IF;

                        --  Insert the final nomination record
                        INSERT INTO nomination (editionID, awardID, filmID, personID, isWinner)
                        VALUES (v_editionID, v_awardID, v_filmID, v_personID, is_winner);

                        -- set a success message
                        SET out_message = CONCAT('Nomination for ''', in_filmTitle, ''' created successfully.');
                    END $$
                    DELIMITER ;


"""

            cursor.execute(query)
            connection.commit()
            print("-Procedure 'InsertFullNomination' created successfully.")
            cursor.close()
            connection.close() # close the connection
    except Error as e:
        print(f"Error creating procedure: {e}")


def procedure_updateWinnerStatus():
    connection = mysql.connector.connect(**DB_CONFIG)

    try:
        if connection.is_connected():
            cursor = connection.cursor()

            # Use the specific database
            DB_usage = f"USE {DB_CONFIG['database']};"
            cursor.execute(DB_usage)

            # Drop the procedure if it already exists
            delete_query = "DROP PROCEDURE IF EXISTS UpdateWinnerStatus;"
            cursor.execute(delete_query)

            # Define the SQL for creating the procedure
            query = """
                    DELIMITER $$
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
                        DECLARE v_nominationID INT;
                        DECLARE v_rowCount INT;

                        -- Find the nominationID based on the provided details
                        SELECT n.nominationID INTO v_nominationID
                        FROM nomination AS n
                        JOIN film AS f ON n.filmID = f.filmID
                        JOIN award AS a ON n.awardID = a.awardID
                        JOIN festivalEdition AS feE ON n.editionID = feE.editionID
                        JOIN festival AS fe ON feE.festivalID = fe.festivalID
                        LEFT JOIN person AS p ON n.personID = p.personID
                        WHERE
                            f.title = in_filmTitle AND
                            a.awardName = in_awardName AND
                            fe.festivalName = in_festivalName AND
                            feE.year = in_editionYear AND
                            -- This condition handles both cases when personName is provided or NULL
                            (in_personName IS NULL OR p.fullName = in_personName)
                        LIMIT 1;

                        -- if matching nomination is found, update its winner status
                        IF v_nominationID IS NOT NULL THEN
                            UPDATE nomination
                            SET isWinner = new_winner_status
                            WHERE nominationID = v_nominationID;

                            SELECT ROW_COUNT() INTO v_rowCount;
                            IF v_rowCount > 0 THEN
                                SET out_message = 'Nomination winner status updated successfully.';
                            ELSE
                                SET out_message = 'No changes made to the nomination winner status.';
                            END IF;
                        ELSE
                            SET out_message = 'No matching nomination found with the provided details.';
                        END IF;
                    END $$
                    DELIMITER ;
                    """
            
            cursor.execute(query)
            connection.commit()
            print("-Procedure 'UpdateWinnerStatus' created successfully.")
            cursor.close()
            connection.close() # close the connection
    except Error as e:
        print(f"Error creating procedure: {e}")

def procedure_deleteFestivalEdition():
    connection = mysql.connector.connect(**DB_CONFIG)

    try:
        if connection.is_connected():
            cursor = connection.cursor()

            # Use the specific database
            DB_usage = f"USE {DB_CONFIG['database']};"
            cursor.execute(DB_usage)

            # Drop the procedure if it already exists
            delete_query = "DROP PROCEDURE IF EXISTS DeleteFestivalEdition;"
            cursor.execute(delete_query)

            # Define the SQL for creating the procedure
            query = """
                    DELIMITER $$

                    CREATE PROCEDURE DeleteFestivalEdition(
                    -- Inout prameter to specify the edition to delete
                    IN in_festivalName VARCHAR(100),
                    IN in_editionYear INT,

                    -- Output parameter to indicate success or failure
                    OUT out_message VARCHAR(255)
                    )

                    BEGIN
                        -- Decalre Variables
                        DECLARE v_editionID INT;
                        DECLARE v_rowCount INT;

                        -- Find the editionID based on the provided festival name and year
                        SELECT feE.editionID INTO v_editionID
                        FROM festivalEdition AS feE
                        JOIN festival AS fe ON feE.festivalID = fe.festivalID
                        WHERE 
                            fe.festivalName = in_festivalName 
                            AND feE.year = in_editionYear
                        LIMIT 1;

                        -- If the edition is found, proceed to delete
                        IF v_editionID IS NOT NULL THEN
                            DELETE FROM festivalEdition WHERE editionID = v_editionID;

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

                    END $$
                    
                    DELIMITER ;
                    """
            
            cursor.execute(query)
            connection.commit()
            print("-Procedure 'DeleteFestivalEdition' created successfully.")
            cursor.close()
            connection.close() # close the connection
    except Error as e:
        print(f"Error creating procedure: {e}")

