# Step-by-Step Project Roadmap

This roadmap breaks the assignment into manageable phases for clarity and progress tracking.

---

## Phase 1: Create the Database Structure (SQL)

**Goal:** Bring your database design to life.

### Write the CREATE TABLE Script
- Create a new `.sql` file (e.g., `01_create_schema.sql`).
- Translate tables from your "Updated Relational Schema" document into `CREATE TABLE` statements.

- **Tip:** Write statements in dependency order:
  - Tables with no foreign keys first
  - Then tables that refer to them

#### Recommended Table Creation Order
1. `Country`, `Genre` *(no dependencies)*
2. `Person`, `Film`, `Festival`, `Award` *(depend on Country)*
3. `Festival_Edition` *(depends on Festival)*
4. `Nomination` *(depends on multiple tables)*
5. `Film_Genre`, `Film_Director`, `Film_Actor` *(linking tables)*

- Double-check all `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, and `UNIQUE` constraints are included.

---

## Phase 2: Populate the Database (Python & SQL)

**Goal:** Read `the_oscar_award.csv` and insert its data into your normalized tables.

> A simple `LOAD DATA INFILE` won't work because the CSV is not structured like your database. Use a Python script for this job.

### Create a Python Script (e.g., `populate_db.py`)
- Use a library like `pandas` or Python's built-in `csv` module to read `the_oscar_award.csv`.
- Use a MySQL connector library (e.g., `mysql-connector-python`) to connect to your database.

#### Data-Import Logic
1. Loop through each row of the CSV file.
2. For each row, get the IDs for the film, person, award, and festival edition.
   - To avoid duplicates, use Python dictionaries to track inserted records.

**Example Logic for One Row:**
```python
# Film
film_title = row['film']
if film_title not in film_lookup:
    # INSERT film into Film table
    # Get LAST_INSERT_ID() and store in dictionary
    film_lookup[film_title] = new_id
else:
    film_id = film_lookup[film_title]
# Repeat similar logic for Person, Award, Festival Edition
```

Person: Do the same for the person's name from the name column and your Person table.

Award: Do the same for the award from the category column and your Award table.

Festival Edition: This is a bit trickier. You'll first need to insert "The Academy Awards" into your Festival table once. Then, for each row, check if an edition for that year_ceremony and ceremony number exists. If not, insert it and get the new edition_id.

Finally: Once you have all the foreign keys (edition_id, award_id, film_id, person_id), INSERT the complete record into the Nomination table, setting is_winner based on the winner column.

## Phase 3: Query Your Data (SQL)

Now that the database is full of data, you can start asking it questions.

### Simple Queries (Level 1)
```sql
SELECT * FROM Film WHERE release_year = 2019;
SELECT full_name FROM Person WHERE full_name LIKE 'Tom%';
```

### Complex Queries (Level 2)
- **Joins:** List all winners for 'Best Picture'. (Join Nomination, Film, and Award)
- **Aggregation:** Which person has the most nominations? (Join Nomination and Person, then use `GROUP BY`, `COUNT()`, and `ORDER BY`)
- **Subqueries:** Find all films that won an award in a year they were not released.

---

## Phase 4 & 5: Add Advanced Features & Connect with Python

Follow the requirements in the assignment specification.

### Advanced SQL
- **Stored Procedure:** Create a procedure that takes a person's name as input and returns a list of all their nominations and wins.
- **View:** Create a view called `vw_WinnerDetails` that pre-joins all the necessary tables to show a clean list of the winner's name, film, award, and year.

### Python Connectivity
- Write a separate, simple Python script that connects to the database.
- Execute one of the complex queries you wrote in Phase 3.
- Fetch the results and print them neatly to the console.
- Demonstrate calling your stored procedure from Python.

---

## Phase 6: Document Everything

**Do not leave this until the end! Document as you go.**

- **User Guide:** Write clear, step-by-step instructions. A classmate should be able to run your `.sql` files and Python scripts and get the same result you do.
- **Report:** Follow the assignment's structure. Explain why you made certain design choices. In your reflection, discuss the challenge of normalizing the CSV data—this is a perfect topic for that section.