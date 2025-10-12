import Database_creation
import Queries

def Menu():
    print("----------------------")
    print("Film festival Database")
    print("----------------------\n")
    
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
    print("8. Exit")
    print("Please select an option (1-5): ")
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
        print("Exiting the program. Goodbye!")
        return True #exit the loop
    else:
        print("Invalid choice. Please select a valid option (1-5).")
        return False #continue the loop