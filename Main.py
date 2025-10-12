import Database_creation
import Menu

#Change these details as per your MySQL configuration from the .env file
#Chnage the file location of teh datasets from the CSV_BASE_PATH variable in Database_creation.py
#name of the sql file to create the database
SQL_File = 'createTables.sql' 

def main():
    isExit = False

    while (not isExit):
        #handle menu system
        userInput = Menu.Menu()
        isExit = Menu.switch_case_menu(userInput , SQL_File)

if __name__ == '__main__':
    main()
