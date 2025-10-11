import Database_creation

def Menu():
    print("----------------------")
    print("Film festival Database")
    print("----------------------\n")
    
    print("If you are a new user, first choose option 0 to create the database and insert data.")
    print("-----------------------")
    print("Menu Options:")
    print("0. CREATE DATABASE & INSERT DATA")
    print("1. Insert data into the database")
    print("2. Query data from the database")
    print("3. Delete data from the database")
    print("4. Update data in the database")
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

    elif choice == 1:
        print("Insert data into the database selected.")

    elif choice == 2:
        print("Query data from the database selected.")
        # Call the function to query data
        # query_data()
    elif choice == 3:
        print("Delete data from the database selected.")
        # Call the function to delete data
        # delete_data()
    elif choice == 4:
        print("Update data in the database selected.")
        # Call the function to update data
        # update_data()
    elif choice == 5:
        print("Exiting the program.")
        exit(0)
    else:
        print("Invalid choice. Please select a valid option (1-5).")