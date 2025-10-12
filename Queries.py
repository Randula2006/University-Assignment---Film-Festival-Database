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

def people_born_after_year(year):
    #Function to query all persons born after a give year by the user

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            query = "SELECT fullName, YEAR(birthDate) AS birthYear FROM person WHERE YEAR(birthDate) > %s ORDER BY birthYear ;"

            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query, (year,)) #tuple with single value
            results = cursor.fetchall()

            # Determining the maximum length of the full names for formatting
            if results:
                max_length_name = max(len(row[0]) for row in results) + 2
            else:
                max_length_name = 0#default value if no results

            print(f"Persons born after {year}:")
            print("===========================================")
            print("|          FullName        |  Birth Year  |")
            print("===========================================")

            for rows in results:
                print(f"| {rows[0]:<{max_length_name}} |     {rows[1]}     |")
            print("===========================================")
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
        
def awards_with_best_in_name():
    #Function to query all awards with "Best" in their name

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            query = "SELECT awardName from award WHERE awardName LIKE '%Best%';"

            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query)
            results = cursor.fetchall()

            # Determining the maximum length of the award names for formatting
            if results:
                max_length_award = max(len(row[0]) for row in results) + 2
            else:
                max_length_award = 0#default value if no results

            print("Awards with 'Best' in their name:")
            print("===================================================")
            print("|                 Award Name                      |")
            print("===================================================")
            for rows in results:
                print(f"| {rows[0]:<{max_length_award}} |")
            print("===================================================")
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

def film_duration(minutes):
    #Function to query all festival edition in a specific year given by the user

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            query = """
                SELECT title, duration 
                FROM film 
                WHERE duration > %s 
                ORDER BY duration DESC; 
            """
            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query, (minutes,)) #tuple with single value
            results = cursor.fetchall()

            # Determining the maximum length of the film titles for formatting
            if results:
                max_length_title = max(len(row[0]) for row in results) + 2
            else:
                max_length_title = 0#default value if no results
            
            print(f"Films longer than {minutes} minutes:")
            print("====================================================================")
            print("|                      Title                      |Duration (mins) |")
            print("====================================================================")
            for rows in results:
                print(f"| {rows[0]:<{max_length_title}} |      {rows[1]}       |")
            print("====================================================================")
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

def films_and_origin_country():
    #Function to query all films and their origin countries

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():

            cursor = connection.cursor()

            query = """
                SELECT f.title AS FilmName, f.releaseYear, c.countryName AS OriginCountry
                FROM film as f INNER JOIN country AS c 
                ON f.countryID = c.countryID
                ORDER BY f.releaseYear DESC;
            """

            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Determining the maximum length of the film titles for formatting
            if results:
                max_length_title = max(len(row[0]) for row in results) + 2
                max_length_country = max(len(row[2]) for row in results) + 2
            else:
                max_length_title = 0#default value if no results
                max_length_country = 0#default value if no results

            print("Films and their Origin Countries:")
            print("===============================================================================================")
            print("|                   Film Name               | Release Year |            Origin Country        |")
            print("===============================================================================================")
            for rows in results:
                print(f"| {rows[0]:<{max_length_title}} |     {rows[1]}     | {rows[2]:<{max_length_country}} |")
            print("===============================================================================================")
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

def all_nominations_details():
    #Function to query all nominations with film, person and award details
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            query = """
                SELECT f.title AS FilmName, p.fullName AS PersonName, a.awardName , fe.festivalName, feE.year, n.isWinner
                FROM nomination AS n INNER JOIN film AS f 
                ON n.filmID = f.filmID 
                LEFT JOIN person AS p ON
                p.personID = n.personID
                INNER JOIN award AS a ON
                a.awardID = n.awardID
                INNER JOIN festivalEdition AS feE ON
                feE.editionID = n.editionID
                INNER JOIN festival AS fe ON
                fe.festivalID = feE.festivalID
                ORDER BY feE.year DESC;   
            """

            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query)

            results = cursor.fetchall()
            # Determining the maximum length of the film titles for formatting
            if results:
                max_length_film = max(len(row[0]) if row[0] is not None else 0 for row in results) + 2
                max_length_person = max(len(row[1]) if row[1] is not None else len("N/A") for row in results) + 2
                max_length_award = max(len(row[2]) if row[2] is not None else 0 for row in results) + 2
                max_length_festival = max(len(row[3]) if row[3] is not None else 0 for row in results) + 2
                max_is_winner = len("Winner") + 3
            else:
                max_length_film = 0#default value if no results
                max_length_person = 0#default value if no results
                max_length_award = 0#default value if no results
                max_length_festival = 0#default value if no results
            
            print("All Nominations with Film, Person and Award Details:")
            print("=====================================================================================================================================================================================")
            print("|             Film Name               |     Person Name    |                    Award Name                   |             Festival Name            | Edition Year |    Is Winner   |")
            print("=====================================================================================================================================================================================")
            for rows in results:
                is_winner_text = "Yes" if rows[5] else "No"
                person_name_text = rows[1] or "N/A"

                print(f"| {rows[0]:<{max_length_film}} | {person_name_text:<{max_length_person}} | {rows[2]:<{max_length_award}} | {rows[3]:<{max_length_festival}} |     {rows[4]}     |   {is_winner_text:<{max_is_winner}}    |")
            print("=====================================================================================================================================================================================")
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

def directors_and_their_films():
    #Function to query all directors and their films
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            query = """
                SELECT p.fullName AS DirectorName, f.title AS FilmName
                FROM filmDirector AS fd INNER JOIN person AS p ON
                p.personID = fd.personID
                INNER JOIN film AS f ON
                f.filmID = fd.filmID
                ORDER BY p.fullName;
            """

            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query)
            results = cursor.fetchall()

            # Determining the maximum length of the director names and film titles for formatting
            if results:
                max_length_director = max(len(row[0]) for row in results) + 2
                max_length_film = max(len(row[1]) for row in results) + 2
            else:
                max_length_director = 0#default value if no results
                max_length_film = 0#default value if no results
            
            print("Directors and their Films:")
            print("=============================================================================")
            print("|      Director Name      |                   Film Name                     |")
            print("=============================================================================")
            for rows in results:
                print(f"| {rows[0]:<{max_length_director}} | {rows[1]:<{max_length_film}} |")
            print("=============================================================================")
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

def actors_in_film(film_title):
    #Function to query all actors in a given film by the user

    try: 
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():

            cursor = connection.cursor()

            query = """
                    SELECT p.fullName AS ActorName, f.title AS FilmTitle
                    FROM filmactor AS fa INNER JOIN person AS p
                    ON fa.personID = p.personID
                    INNER JOIN film AS f
                    ON fa.filmID = f.filmID
                    WHERE f.title = %s;
                """
            
            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query, (film_title,)) #tuple with single value
            results = cursor.fetchall()

            # Determining the maximum length of the actor names for formatting
            if results:
                max_length_actor = max(len(row[0]) for row in results) + 2
            else:
                max_length_actor = 0#default value if no results

            print(f"Actors in the film '{film_title}':")
            print("===================================")
            print("|     Actor Name   |  Film Title  |")
            print("===================================")
            for rows in results:
                print(f"| {rows[0]:<{max_length_actor}} | {rows[1]} |")
            print("===================================")
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

def total_number_of_films_per_country():
    #Function to query total number of films per country

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            query = """
                SELECT c.countryName, COUNT(f.filmID) AS TotalFilms
                FROM country AS c LEFT JOIN film as f
                ON c.countryID = f.countryID
                GROUP BY c.countryName
                ORDER BY TotalFilms DESC;
                """

            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query)

            results = cursor.fetchall()

            # Determining the maximum length of the country names for formatting
            if results:
                max_length_country = max(len(row[0]) for row in results) + 1
            else:
                max_length_country = 0#default value if no results
            print("Total Number of Films per Country:")
            print("===================================================")
            print("|        Country Name       |Total Number of Films|")
            print("===================================================")
            for rows in results:
                print(f"| {rows[0]:<{max_length_country}} |          {rows[1]}          |")
            print("===================================================")
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

def number_of_nominations_per_film():
    #Function to query number of nomination per film

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            query = """
                    SELECT f.title AS FilmName, COUNT(n.nominationID) AS TotalNominations
                    FROM film AS f LEFT JOIN nomination AS n
                    ON f.filmID = n.filmID
                    WHERE n.nominationID > 0
                    GROUP BY f.title
                    ORDER BY TotalNominations DESC;
            """
            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query)

            results = cursor.fetchall()
            # Determining the maximum length of the person names for formatting
            if results:
                max_length_person = max(len(row[0]) for row in results) + 2
            else:
                max_length_person = 0#default value if no results
            print("Number of Nominations per Person:")
            print("==============================================================")
            print("|            Person Name         |Total Number of Nominations|")
            print("==============================================================")
            for rows in results:
                print(f"| {rows[0]:<{max_length_person}} |          {rows[1]}          |")
            print("==============================================================")
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

def average_duration_of_films_per_genre():
    #Function to query average duration of films per genre

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            query = """
                    SELECT g.genreName, AVG(f.duration) AS AverageDuration
                    FROM genre AS g LEFT JOIN filmgenre AS fg
                    ON g.genreID = fg.genreID
                    LEFT JOIN film AS f
                    ON fg.filmID = f.filmID
                    GROUP BY g.genreName
                    ORDER BY AverageDuration DESC;
            """
            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query)

            results = cursor.fetchall()

            # Determining the maximum length of the genre names for formatting
            if results:
                max_length_genre = max(len(row[0]) for row in results) + 2
            else:
                max_length_genre = 0#default value if no results

            print("Average Duration of Films per Genre:")
            print("================================================")
            print("|     Genre Name    | Average Duration (mins)  |")
            print("================================================")
            for rows in results:
                print(f"| {rows[0]:<{max_length_genre}} |          {rows[1]:.2f}          |")
            print("================================================")

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

def awards_given_out_by_festival_edition():
    #Function to query awards given out by each festival edition
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():

            cursor = connection.cursor()

            query = """
                    SELECT f.festivalName, fe.year, COUNT(n.nominationID) AS TotalAwardsGiven
                    FROM festival AS f INNER JOIN festivalEdition AS fe
                    ON f.festivalID = fe.festivalID
                    LEFT JOIN nomination AS n
                    ON fe.editionID = n.editionID AND n.isWinner = TRUE
                    GROUP BY f.festivalName, fe.year
                    ORDER BY fe.year DESC , TotalAwardsGiven DESC;
            """

            cursor.execute(DB_usage) #use the specific database
            cursor.execute(query)
            results = cursor.fetchall()

            # Determining the maximum length of the festival names for formatting
            if results:
                max_length_festival = max(len(row[0]) for row in results) + 2
            else:
                max_length_festival = 0#default value if no results

            print("Awards Given Out by Each Festival Edition:")
            print("============================================================================")
            print("|             Festival Name            | Edition Year | Total Awards Given |")
            print("============================================================================")
            for rows in results:
                print(f"| {rows[0]:<{max_length_festival}} |     {rows[1]}     |         {rows[2]}         |")
            print("============================================================================")
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

    
