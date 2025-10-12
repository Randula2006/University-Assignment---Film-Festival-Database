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
    print("2. Query: All films and their release year")
    print("3. Query: Find all persons born after a given year")
    print("4. Query: Awards with 'Best' in their name")
    print("5. Exit")
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
        print("Exiting the program.")
        exit(0)
        return True #exit the loop
    else:
        print("Invalid choice. Please select a valid option (1-5).")
        return False #continue the loop