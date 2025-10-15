-- =====================================================================
--          Film Festival Database Schema
-- =====================================================================
-- This script creates the database and all necessary tables for the
-- film festival management system.

-- First, drop the database if it already exists to ensure a clean setup.
DROP DATABASE IF EXISTS Gunathilake_23610903;

-- Create the new database.
CREATE DATABASE Gunathilake_23610903;

-- Select the newly created database to work with.
USE Gunathilake_23610903;


-- Stores country information. Referenced by people, festivals, and films.
CREATE TABLE Country(
    countryID INT AUTO_INCREMENT, -- Unique identifier for each country.
    countryName VARCHAR(100) NOT NULL UNIQUE, -- The full name of the country (e.g., 'USA').
    countryCode CHAR(3) NOT NULL UNIQUE, -- The 3-letter ISO code for the country (e.g., 'USA').
    PRIMARY KEY (countryID) 
);

-- Stores different film genres.
CREATE TABLE Genre(
    genreID INT AUTO_INCREMENT, -- Unique identifier for each genre.
    genreName VARCHAR(100) NOT NULL UNIQUE, -- The name of the genre (e.g., 'Action', 'Drama').
    PRIMARY KEY (genreID)
);

-- Stores the names of different awards given at festivals.
CREATE TABLE Award(
    awardID int AUTO_INCREMENT, -- Unique identifier for each award.
    awardName VARCHAR(255) NOT NULL UNIQUE, -- The name of the award (e.g., "Palme d'Or").
    PRIMARY KEY (awardID)
);

-- Stores information about individuals like actors and directors.
CREATE TABLE Person(
    personID int PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each person.
    fullName VARCHAR(100) NOT NULL, -- The full name of the person.
    birthDate DATE, -- The person's date of birth.
    countryID INT, -- A foreign key linking to the person's country of origin.
    FOREIGN KEY (countryID) REFERENCES Country(countryID)
        ON DELETE SET NULL -- If a country is deleted, the person's country is set to NULL, preserving the person's record.
        ON UPDATE CASCADE -- If a countryID is updated, all references in this table are updated too.
);

-- Stores main information about each film festival.
CREATE TABLE Festival(
    festivalID INT AUTO_INCREMENT, -- Unique identifier for each festival.
    festivalName VARCHAR(100) NOT NULL UNIQUE, -- The name of the festival (e.g., 'Cannes Film Festival').
    countryID INT NOT NULL, -- A foreign key linking to the country where the festival is held.
    PRIMARY KEY (festivalID),
    FOREIGN KEY (countryID) REFERENCES Country(countryID)
        ON DELETE RESTRICT -- Prevents a country from being deleted if a festival is associated with it. This maintains data integrity.
        ON UPDATE CASCADE -- If a countryID is updated, all references here are updated.
);

-- Stores information about each film.
CREATE TABLE Film(
    filmID INT AUTO_INCREMENT, -- Unique identifier for each film.
    title VARCHAR(200) NOT NULL, -- The title of the film.
    releaseYear INT, -- The year the film was released.
    duration INT, -- The duration of the film in minutes.
    countryID INT, -- A foreign key linking to the film's country of origin.
    rating DECIMAL(3,1) CHECK (rating >= 0 AND rating <= 10), -- The film's rating, constrained between 0 and 10.
    PRIMARY KEY (filmID),
    FOREIGN KEY (countryID) REFERENCES Country(countryID)
        ON DELETE SET NULL -- If a country is deleted, the film's country is set to NULL, preserving the film's record.
        ON UPDATE CASCADE -- If a countryID is updated, all references here are updated.
);

-- Stores information about specific editions of a festival (e.g., Cannes 2023).
CREATE TABLE FestivalEdition(
    editionID INT AUTO_INCREMENT, -- Unique identifier for each festival edition.
    festivalID INT NOT NULL, -- A foreign key linking to the parent festival.
    year INT NOT NULL, -- The year of this edition.
    ceremonyNumber INT, -- The number of the ceremony (e.g., 76th). This was corrected from "ceromanyNumber".
    startDate DATE NOT NULL, -- The start date of the festival edition.
    endDate DATE NOT NULL, -- The end date of the festival edition.
    PRIMARY KEY (editionID),
    FOREIGN KEY (festivalID) REFERENCES Festival(festivalID)
        ON DELETE CASCADE -- If a festival is deleted, all its historical editions are also deleted.
        ON UPDATE CASCADE, -- If a festivalID is updated, all its editions are updated too.
    CHECK (endDate >= startDate) -- Ensures the end date is not before the start date.
);

-- =====================================================================
--                          JUNCTION TABLES
-- =====================================================================

-- Manages the Many-to-Many relationship between films and genres.
CREATE TABLE FilmGenre(
    filmID INT, -- Foreign key to the Film table.
    genreID INT, -- Foreign key to the Genre table.
    PRIMARY KEY (filmID, genreID), -- Composite primary key to ensure each film-genre pair is unique.
    FOREIGN KEY (filmID) REFERENCES Film(filmID)
        ON DELETE CASCADE -- If a film is deleted, its genre associations are also deleted.
        ON UPDATE CASCADE,
    FOREIGN KEY (genreID) REFERENCES Genre(genreID)
        ON DELETE CASCADE -- If a genre is deleted, its associations with films are also deleted.
        ON UPDATE CASCADE
);

-- Manages all nominations for awards at each festival edition.
CREATE TABLE Nomination(
    nominationID INT AUTO_INCREMENT, -- Unique identifier for each nomination.
    editionID INT NOT NULL, -- Foreign key linking to a specific festival edition.
    awardID INT NOT NULL, -- Foreign key linking to the award being nominated for.
    filmID INT NOT NULL, -- Foreign key linking to the nominated film.
    personID INT, -- Foreign key linking to a nominated person. Can be NULL for film-level awards (e.g., 'Best Picture').
    isWinner BOOLEAN DEFAULT FALSE, -- A flag (TRUE/FALSE or 1/0) to indicate if the nomination won the award.
    PRIMARY KEY (nominationID),
    FOREIGN KEY (awardID) REFERENCES Award(awardID)
        ON DELETE RESTRICT -- Prevents deleting an award if it has nominations, preserving historical data.
        ON UPDATE CASCADE,
    FOREIGN KEY (filmID) REFERENCES Film(filmID)
        ON DELETE RESTRICT -- Prevents deleting a film if it has nominations, preserving historical data.
        ON UPDATE CASCADE,
    FOREIGN KEY (personID) REFERENCES Person(personID)
        ON DELETE SET NULL -- If a person is deleted, the nomination record remains but the personID becomes NULL.
        ON UPDATE CASCADE
);

-- Manages the Many-to-Many relationship between films and directors (who are 'Person' records).
CREATE TABLE FilmDirector(
    filmID INT, -- Foreign key to the Film table.
    personID INT, -- Foreign key to the Person table (representing a director).
    PRIMARY KEY (filmID, personID), -- Composite primary key.
    FOREIGN KEY (filmID) REFERENCES Film(filmID)
        ON DELETE CASCADE -- If a film is deleted, its director associations are also deleted.
        ON UPDATE CASCADE,
    FOREIGN KEY (personID) REFERENCES Person(personID)
        ON DELETE CASCADE -- If a person is deleted, their director credits are also deleted.
        ON UPDATE CASCADE
);

-- Manages the Many-to-Many relationship between films and actors (who are 'Person' records).
CREATE TABLE FilmActor(
    filmID INT, -- Foreign key to the Film table.
    personID INT, -- Foreign key to the Person table (representing an actor).
    PRIMARY KEY (filmID, personID), -- Composite primary key.
    FOREIGN KEY (filmID) REFERENCES Film(filmID)
        ON DELETE CASCADE -- If a film is deleted, its actor associations are also deleted.
        ON UPDATE CASCADE,
    FOREIGN KEY (personID) REFERENCES Person(personID)
        ON DELETE CASCADE -- If a person is deleted, their acting credits are also deleted.
        ON UPDATE CASCADE
);

-- Made by Randula Gunathilake