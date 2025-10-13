import Database_creation
import Queries

def Menu():
    print("-------------------------------------")
    print("Welcome to the Film festival Database")
    print("-------------------------------------\n")
    
    print("If you are a new user, first choose option 0 to create the database and insert data.")
    print("-----------------------")
    print("Menu Options:")
    print("0. CREATE DATABASE & INSERT DATA")
    print("1. Insert data into the database")
    print("2. Simple-Query: All films and their release year")
    print("3. Simple-Query: Find all persons born after a given year")
    print("4. Simple-Query: Awards with 'Best' in their name")
    print("5. Simple-Query: Films that are longer than a given duration")
    print("-----------------------")
    print("6. Advanced-Query: Films and their Origin Country")
    print("7. Advanced-Query: All nominations with film, person and award details")
    print("8. Advanced-Query: Directors and their films")
    print("9. Advanced-Query: Actors in a gicen film")
    print("-----------------------")
    print("10. Aggregate-Query: Total Number of Films per country")
    print("11. Aggregate-Query: Number of nomination per film")
    print("12. Aggregate-Query: Avarage duration of films per genre")
    print("13. Aggregate-Query: Awards given out by each festival edition")
    print("-----------------------")
    print("14. Sub-Query: Films longer than the avarage duration")
    print("15. Sub-Query: Direcotrs of award winning films")
    print("16. Sub-Query: Actors who starred in Palme d'Or winning films")
    print("17. Festival where a specific Film was nominated")
    print("18. Director who have not won 'Best Director' award")
    print("-----------------------")
    print("19. View: Show all Winners")
    print("20. View: Show Summery of Films")
    print("-----------------------")
    print("21. Procedure: Get Person Award History")
    print("22. Procedure: Insert Full Nomination")
    print("23. Procedure: Update Winner Status")
    print("24. Procedure: Delete Festival Edition")
    print("25. Exit")
    print("Please select an option (0-25): ")
    choice = int(input())
    
    if (type(choice) is not int) and (choice < 1 or choice > 5 or choice is None):
        print("Invalid choice. Please select a valid option (1-5).")
        return Menu()
    
    return choice


def switch_case_menu(choice, SQL_File):
    # Function to handle user choices from the menu.
    if choice == 0:
        print("Create database and insert data selected.")
        print("-----------------------------------------")
        #This happens only for the new users
        # Call the function to create the database and insert data
        Database_creation.create_database(SQL_File)
        Database_creation.insert_data_into_db()
        Database_creation.create_indexes()
        Database_creation.create_view_AllWinners()
        Database_creation.create_view_FilmSummary()
        Database_creation.alter_film_table()
        Database_creation.Trigger_after_nomination_insert()
        Database_creation.Trigger_prevent_winner_deletion()
        Database_creation.procedure_getPersonAwardHistory()
        Database_creation.procedure_InsertFullNomination()
        Database_creation.procedure_updateWinnerStatus()
        Database_creation.procedure_deleteFestivalEdition()
        return False #continue the loop

    elif choice == 1:
        print("Insert data into the database selected.")

    elif choice == 2:
        print("Query All films and their release year selected.")
        print("--------------------------------------------------------------------------")
        # Call the function to query films and their release years
        Queries.Films_and_years()
        return False #continue the loop
    
    elif choice == 3:
        input_year = int(input("Enter the year to find persons born after that year: "))
        # Call the function to query persons born after the given year
        Queries.people_born_after_year(input_year)
        return False #continue the loop
    
    elif choice == 4:
        print("Query Awards with 'Best' in their name selected.")
        # Call the function to query awards with 'Best' in their name
        Queries.awards_with_best_in_name()
        return False #continue the loop
    
    elif choice == 5:
        input_mins = int(input("Enter the duration (in minutes) to find films longer than that duration: "))
        # Call the function to query festival editions in the given year
        Queries.film_duration(input_mins)
        return False #continue the loop
    
    elif choice == 6:
        print("Query Films and their Origin Country selected.")
        # Call the function to query films and their origin countries
        Queries.films_and_origin_country()
        return False #continue the loop
    
    elif choice == 7:
        print("Query All nominations with film, person and award details selected.")
        # Call the function to query all nominations with film, person and award details
        Queries.all_nominations_details()
        return False #continue the loop
    
    elif choice == 8:
        print("Query Directors and their films selected.")
        # Call the function to query directors and their films
        Queries.directors_and_their_films()
        return False #continue the loop
    
    elif choice == 9:
        input_film = input("Enter the film title to find actors in that film:")
        # Call the function to query actors in the given film
        Queries.actors_in_film(input_film)
        return False #continue the loop
    
    elif choice == 10:
        print("Query Total Number of Films per country selected.")
        # Call the function to query total number of films per country
        Queries.total_number_of_films_per_country()
        return False #continue the loop
    
    elif choice == 11:
        print("Query Number of nomination per film selected.")
        # Call the function to query number of nominations per person
        Queries.number_of_nominations_per_film()
        return False #continue the loop
    
    elif choice == 12:
        print("Query Avarage duration of films per genre selected.")
        # Call the function to query average duration of films per genre
        Queries.average_duration_of_films_per_genre()
        return False #continue the loop
    
    elif choice == 13:
        print("Query Awards given out by each festival edition selected.")
        # Call the function to query awards given out by each festival edition
        Queries.awards_given_out_by_festival_edition()
        return False #continue the loop
    
    elif choice == 14:
        print("Query Films longer than the average duration selected.")
        # Call the function to query persons with multiple awards
        Queries.films_longer_than_average_duration()
        return False #continue the loop
    
    elif choice == 15:
        print("Query Directors of award winning films selected.")
        # Call the function to query directors of award winning films
        Queries.directors_of_award_winning_films()
        return False #continue the loop
    
    elif choice == 16:
        print("Query Actors who starred in Palme d'Or winning films selected.")
        # Call the function to query actors who starred in Palme d'Or winning films
        Queries.actors_in_palme_dor_winning_films()
        return False #continue the loop
    
    elif choice == 17:
        input_film = input("Enter the film title to find the festival where it was nominated: ")
        # Call the function to query festival where a specific film was nominated
        Queries.festival_where_film_nominated(input_film)
        return False #continue the loop
    
    elif choice == 18:
        print("Query Directors who have not won 'Best Director' award selected.")
        # Call the function to query directors who have not won 'Best Director' award
        Queries.directors_without_best_director_award()
        return False #continue the loop
    
    elif choice == 19:
        print("View: Show all Winners selected.")
        # Call the function to display all winners from the view
        Queries.show_all_winners()
        return False #continue the loop
    
    elif choice == 20:
        print("View: Show Summery of Films selected.")
        # Call the function to display summery of films from the view
        Queries.show_summary_of_films()
        return False #continue the loop
    
    elif choice == 21:
        input_person = input("Enter the person's name to get their award history: ")
        # Call the function to execute the stored procedure to get person's award history
        Queries.get_person_award_history(input_person)
        return False #continue the loop
    
    elif choice == 22:
        print("Procedure: Insert Full Nomination selected.")
        # Call the function to execute the stored procedure to insert a full nomination
                    # Collecting all necessary inputs from the user
        film_title = input("Enter Film Title: ")
        film_duration = int(input("Enter Film Duration (in minutes): "))
        film_release_year = int(input("Enter Film Release Year (e.g., 2023): "))
        person_name = input("Enter Director's Full Name: ")
        person_birthdate = input("Enter Director's Birth Date (YYYY-MM-DD): ")
        person_country = input("Enter Director's Country: ")
        person_countryCode = input("Enter Director's Country Code (e.g., US, FR): ")

        award_name = input("Enter Award Name: ")
        festival_name = input("Enter Festival Name: ")
        festival_country = input("Enter Festival Country: ")
        festival_countryCode = input("Enter Festival Country Code (e.g., US, FR): ")
        edition_ceromany_num = int(input("Enter Festival Edition Ceromany Number (e.g., 75): "))
        edition_year = int(input("Enter Festival Edition Year (e.g., 2023): "))
        edition_start_date = input("Enter Festival Edition Start Date (YYYY-MM-DD): ")
        edition_end_date = input("Enter Festival Edition End Date (YYYY-MM-DD): ")
        is_winner_input = input("Is this nomination a winner? (yes/no): ").strip().lower()

        Queries.insert_full_nomination(film_title, film_release_year, film_duration,
                                       person_name, person_birthdate, person_country, person_countryCode,
                                       award_name, festival_name, festival_country, festival_countryCode,
                                       edition_year, edition_ceromany_num, edition_start_date, edition_end_date,
                                       is_winner_input)
        
        return False #continue the loop
    
    elif choice == 23:
        print("Procedure: Update Winner Status selected.")
        film_title = input("Enter the film title of the nomination: ")
        award_name = input("Enter the award name of the nomination: ")
        festival_name = input("Enter the festival name of the nomination: ")
        edition_year = int(input("Enter the edition year of the nomination (e.g., 2023): "))
        person_name = input("Enter the person's full name associated with the nomination: ")
        new_status_input = input("Enter the new winner status (yes/no): ").strip().lower()

        Queries.update_winner_status(film_title, award_name, festival_name, edition_year, person_name, new_status_input)
        return False #continue the loop
    
    elif choice == 24:
        print("Procedure: Delete Festival Edition selected.")
        festival_name = input("Enter the festival name of the edition you want to delete: ")
        edition_year = int(input("Enter the year of the edition you want to delete (e.g., 2023): "))
        Queries.delete_festival_edition(festival_name, edition_year)
        return False #continue the loop
    
    elif choice == 25:
        print("Exiting the program. Goodbye!")
        return True #exit the loop
    
    else:
        print("Invalid choice. Please select a valid option (1-5).")
        return False #continue the loop