
-- TABLE CREATION 

CREATE TABLE FestivalEdition(
    editionID INT PRIMARY KEY,
    festivalID INT,
    year INT,
    ceromanyNumber INT,
    startDate DATE,
    endDate DATE,
    FOREIGN KEY (festivalID) REFERENCES Festival(festivalID)
);

CREATE TABLE Award(
    awardID int PRIMARY KEY,
    awardName VARCHAR(100) NOT NULL,

);

CREATE TABLE Nomination(
    nominationID INT PRIMARY KEY,
    editionID INT,
    awardID INT,
    filmID INT,
    personID INT,
    isWinner BOOLEAN NOT NULL,
    -- use values from a predifined list
    -- result ENUM('Won', 'Nominated') NOT NULL,
    FOREIGN KEY (editionID) REFERENCES FestivalEdition(editionID),
    FOREIGN KEY (awardID) REFERENCES Award(awardID),
    FOREIGN KEY (filmID) REFERENCES Film(filmID),
    FOREIGN KEY (personID) REFERENCES Person(personID)
);

CREATE TABLE FilmGenre(
    filmID INT,
    genreID INT,
    PRIMARY KEY (filmID, genreID),
    FOREIGN KEY (filmID) REFERENCES Film(filmID),
    FOREIGN KEY (genreID) REFERENCES Genre(genreID)
);

CREATE TABLE FilmDirector(
    filmID INT,
    personID INT,
    PRIMARY KEY (filmID, personID),
    FOREIGN KEY (filmID) REFERENCES Film(filmID),
    FOREIGN KEY (personID) REFERENCES Person(personID)
);

CREATE TABLE FilmActor(
    filmID INT,
    personID INT,
    PRIMARY KEY (filmID, personID),
    FOREIGN KEY (filmID) REFERENCES Film(filmID),
    FOREIGN KEY (personID) REFERENCES Person(personID)
);

CREATE TABLE Country(
    countryID INT PRIMARY KEY,
    -- there are no countrues with the same name -- so uniqe constraint can be used
    countryName VARCHAR(100) NOT NULL UNIQUE 
);

CREATE TABLE Person(
    personID int PRIMARY KEY,
    fullName VARCHAR(100) NOT NULL,
    birthDate DATE,
    countryID INT,
    FOREIGN KEY (countryID) REFERENCES Country(countryID)
);

CREATE TABLE Film(
    filmID INT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    releaseYear INT,
    duration INT,
    countryID INT,
    FOREIGN KEY (countryID) REFERENCES Country(countryID)
);

CREATE TABLE Genre(
    genreID INT PRIMARY KEY,
    genreName VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Festival(
    festivalID INT PRIMARY KEY,
    festivalName VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(100) NOT NULL
);
