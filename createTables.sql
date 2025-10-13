-- Database Creation
-- Database Source

DROP DATABASE IF EXISTS Gunathilake_23610903;
CREATE DATABASE Gunathilake_23610903;
USE Gunathilake_23610903;

-- TABLE CREATION 
-- Countries (country information)
CREATE TABLE Country(
    countryID INT AUTO_INCREMENT, -- there are no countrues with the same name -- so uniqe constraint can be used
    countryName VARCHAR(100) NOT NULL UNIQUE,
    countryCode CHAR(3) NOT NULL UNIQUE,
    PRIMARY KEY (countryID) 
);

-- Genres (Different film genres)
CREATE TABLE Genre(
    genreID INT AUTO_INCREMENT,
    genreName VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (genreID)
);

-- Awards (Different awards given at the festival)
CREATE TABLE Award(
    awardID int AUTO_INCREMENT,
    awardName VARCHAR(100) NOT NULL,
    PRIMARY KEY (awardID)
);

-- People (Directors, Actors, etc.)
CREATE TABLE Person(
    personID int PRIMARY KEY AUTO_INCREMENT,
    fullName VARCHAR(100) NOT NULL,
    birthDate DATE,
    countryID INT,
    FOREIGN KEY (countryID) REFERENCES Country(countryID)
        ON DELETE SET NULL -- if a country is deleted, the countryID in Person is set to NULL
        ON UPDATE CASCADE -- if a countryID is updated, all its persons are updated too 
);

-- film festivals (Main festival information)
CREATE TABLE Festival(
    festivalID INT AUTO_INCREMENT,
    festivalName VARCHAR(100) NOT NULL UNIQUE,
    countryID INT NOT NULL,
    PRIMARY KEY (festivalID),
    FOREIGN KEY (countryID) REFERENCES Country(countryID)
        ON DELETE RESTRICT -- if a country is deleted, the countryID in Festival is set to NULL
        ON UPDATE CASCADE -- if a countryID is updated, all its festivals are updated too
);

-- Films (Film information)
CREATE TABLE Film(
    filmID INT AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    releaseYear INT,
    duration INT,
    countryID INT,
    rating DECIMAL(3,1) CHECK (rating >= 0 AND rating <= 10), -- rating between 0 and 10
    PRIMARY KEY (filmID),
    FOREIGN KEY (countryID) REFERENCES Country(countryID)
        ON DELETE SET NULL -- if a country is deleted, the countryID in Film is set to NULL
        ON UPDATE CASCADE -- if a countryID is updated, all its films are updated too   
);

-- Festival editions (Each year a festival is held, it is considered a new edition)
CREATE TABLE FestivalEdition(
    editionID INT AUTO_INCREMENT,
    festivalID INT NOT NULL,
    year INT NOT NULL,
    ceromanyNumber INT,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    PRIMARY KEY (editionID),
    FOREIGN KEY (festivalID) REFERENCES Festival(festivalID)
        ON DELETE CASCADE -- if a festival is deleted, all its editions are deleted too
        ON UPDATE CASCADE, -- if a festivalID is updated, all its editions are updated too  
    CHECK (endDate >= startDate)
);

-- FilmGenre (Many-to-Many relationship between films and genres)
CREATE TABLE FilmGenre(
    filmID INT,
    genreID INT,
    PRIMARY KEY (filmID, genreID),
    FOREIGN KEY (filmID) REFERENCES Film(filmID)
        ON DELETE CASCADE -- if a film is deleted, all its genres are deleted too
        ON UPDATE CASCADE, -- if a filmID is updated, all its genres are updated
    FOREIGN KEY (genreID) REFERENCES Genre(genreID)
        ON DELETE CASCADE -- if a genre is deleted, all its films are deleted too
        ON UPDATE CASCADE  -- if a genreID is updated, all its films are updated
);

-- Nominations (Nominations for awards in each festival edition)
CREATE TABLE Nomination(
    nominationID INT AUTO_INCREMENT,
    editionID INT NOT NULL,
    awardID INT NOT NULL,
    filmID INT NOT NULL,
    personID INT, -- Null for film awards, NOT NUll for individual awards
    isWinner BOOLEAN DEFAULT FALSE, -- TRUE if the nomination won the award
    PRIMARY KEY (nominationID),
    FOREIGN KEY (editionID) REFERENCES FestivalEdition(editionID)
        ON DELETE CASCADE -- if a festival edition is deleted, all its nominations are deleted too
        ON UPDATE CASCADE, -- if a festival editionID is updated, all its nominations are updated too
    FOREIGN KEY (awardID) REFERENCES Award(awardID)
        ON DELETE CASCADE -- if a festival edition is deleted, all its nominations are deleted too
        ON UPDATE CASCADE, -- if a festival editionID is updated, all its nominations are updated too
    FOREIGN KEY (filmID) REFERENCES Film(filmID)
        ON DELETE CASCADE -- if a festival edition is deleted, all its nominations are deleted too
        ON UPDATE CASCADE, -- if a festival editionID is updated, all its nominations are updated too
    FOREIGN KEY (personID) REFERENCES Person(personID)
        ON DELETE CASCADE -- if a festival edition is deleted, all its nominations are deleted too
        ON UPDATE CASCADE -- if a festival editionID is updated, all its nominations are updated too
);


-- FilmDirector (Many-to-Many relationship between films and person)
CREATE TABLE FilmDirector(
    filmID INT,
    personID INT,
    PRIMARY KEY (filmID, personID),
    FOREIGN KEY (filmID) REFERENCES Film(filmID)
        ON DELETE CASCADE -- if a film is deleted, all its directors are deleted too
        ON UPDATE CASCADE, -- if a filmID is updated, all its directors are updated
    FOREIGN KEY (personID) REFERENCES Person(personID)
        ON DELETE CASCADE -- if a person is deleted, all its films are deleted too
        ON UPDATE CASCADE  -- if a personID is updated, all its films are updated
);

-- FilmActor (Many-to-Many relationship between films and person)
CREATE TABLE FilmActor(
    filmID INT,
    personID INT,
    PRIMARY KEY (filmID, personID),
    FOREIGN KEY (filmID) REFERENCES Film(filmID)
        ON DELETE CASCADE -- if a film is deleted, all its actors are deleted too
        ON UPDATE CASCADE, -- if a filmID is updated, all its actors are updated
    FOREIGN KEY (personID) REFERENCES Person(personID)
        ON DELETE CASCADE -- if a person is deleted, all its films are deleted too
        ON UPDATE CASCADE  -- if a personID is updated, all its films are updated
);




