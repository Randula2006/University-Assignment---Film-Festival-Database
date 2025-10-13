#  Film Festival Database - Database Systems Assignment

This is my project for the Database Systems unit. It's a command-line application written in Python that manages a database for a film festival. You can do a bunch of stuff like create the whole database from scratch, fill it with data, and run all sorts of queries.

##  What's Inside?

Features this project has:

*   **Full Database Setup**: The script creates the database, all the tables, and sets up the relationships.
*   **Data Import**: It automatically reads data from CSV files and populates the database.
*   **Interactive Menu**: A user-friendly menu to navigate through all the features.
*   **Lots of Queries**:
    *   **Simple Queries**: Basic lookups like finding films or people.
    *   **Advanced Queries**: More complex stuff using `JOIN`s.
    *   **Aggregate Queries**: Queries that calculate totals, averages, etc. (`GROUP BY`).
    *   **Sub-Queries**: Queries within queries!
*   **Advanced SQL Stuff**:
    *   **Views**: To simplify complex queries.
    *   **Stored Procedures**: To run pre-compiled SQL code for common tasks like adding a full nomination or updating a winner.
    *   **Triggers**: To automate things, like updating a count when a new nomination is added.

##  Getting Started

To get this running on your machine, you'll need to do a few things first.

### 1. Prerequisites

Make sure you have these installed:

*   **Python 3**: You can get it from the official Python website.
*   **MySQL Server**: You need a running MySQL server. You can use something like XAMPP, MAMP, or install it directly.
*   **Python Libraries**: You'll need a couple of Python packages. You can install them using pip:

    ```bash
    pip install mysql-connector-python python-dotenv
    ```

### 2. Configuration

**This is the most important step!** The script needs to know how to connect to your database and where your data files are.

1.  **Create a `.env` file**: In the same directory as the Python scripts, create a new file and name it `.env`.

2.  **Add your details**: Copy the text below into your new `.env` file and change the values to match your own setup.

    ```
    # Your MySQL Database Details
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_mysql_password
    DB_NAME=Gunathilake_23610903
    
    # Path to the folder with all the .csv data files
    # IMPORTANT: Use forward slashes '/' even on Windows!
    FILE_PATH=D:/Curtin University/Database Systems/Database Assignment/FinalDatasets/
    
    # The name of the SQL file for creating tables
    SQL_FILE=createTables.sql
    ```

    **A quick note:**
    *   `DB_PASSWORD`: If you don't have a password for MySQL (like with a default XAMPP setup), just leave it blank: `DB_PASSWORD=`.
    *   `FILE_PATH`: Make sure this path points to the folder where you've saved all the `_data.csv` files.

### 3. The Data

Make sure all your CSV files (like `film_data.csv`, `person_data.csv`, etc.) are in the folder you specified in the `FILE_PATH` variable in your `.env` file.

##  How to Run the Application

Once you've done the setup, running it is easy.

1.  Open your terminal or command prompt.
2.  Navigate to the project directory.
3.  Run the `Main.py` script:

    ```bash
    python Main.py
    ```

##  Using the Menu

You'll be greeted with a big menu of options.

### First-Time Use

If this is your first time running the program, **you MUST select option `0`**.

> **0. CREATE DATABASE & INSERT DATA**

This option will:
1.  Connect to your MySQL server.
2.  Create the database (`Gunathilake_23610903`).
3.  Create all the tables from `createTables.sql`.
4.  Insert all the data from your CSV files.
5.  Create the views, triggers, and stored procedures.

It might take a moment, but you'll see progress messages in the console. You only need to do this once!

### Exploring the Database

After the initial setup, you can restart the program and choose any other option from `1` to `25` to explore the database. Some options will ask you for input, like a year or a film title. Just type in your answer and press Enter.

To quit the program, just choose option `25`.

---

Made by Randula Gunathilake