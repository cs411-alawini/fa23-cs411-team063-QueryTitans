CREATE TABLE Laptop (
    Laptop_Id varchar(64) PRIMARY KEY,
    Brand Varchar(64) NOT NULL,
    Model Varchar(64) NOT NULL,
    Operating_System VARCHAR(64) NOT NULL,
    Processor_Speed INT NOT NULL,
    RAM INT NOT NULL,
    Graphics INT NOT NULL,
    Laptop_Rating Decimal(5,2) GENERATED ALWAYS AS 
        (
            (
                (Processor_Speed * 0.4) + (RAM * 0.3) + (Graphics * 0.3)
            ) 
            / 15.7 * 5 
        ) VIRTUAL
);

##User Table
CREATE TABLE User (
    User_Id varchar(16) PRIMARY KEY,
    First_Name VARCHAR(64) NOT NULL,
    Last_Name VARCHAR(64) NOT NULL,
    Pass_Word VARCHAR(64) NOT NULL,
    Date_of_Birth DATE,
    Age INT,
    Email VARCHAR(64) NOT NULL,
    Preferred_Genre VARCHAR(64),
    Preferred_Category VARCHAR(64),
    User_Type ENUM('Individual', 'Organizer') NOT NULL,
    Laptop_Id varchar(64),
    FOREIGN KEY (Laptop_Id) REFERENCES Laptop(Laptop_Id) ON DELETE SET NULL
);


##Trigger to calculate Age in User Table
DELIMITER //
CREATE TRIGGER calculate_age
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
  IF NEW.Date_of_Birth IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Date_of_Birth cannot be NULL';
  ELSE
    SET NEW.Age = FLOOR(DATEDIFF(CURDATE(), NEW.Date_of_Birth) / 365);
  END IF;
END;
//
DELIMITER ;

##Game Table
CREATE TABLE Game (
    Game_Id varchar(64) PRIMARY KEY,
    Game_Name text NOT NULL,
    Date_of_Release DATE,
    Price real NOT NULL,
    Genre VARCHAR(64) NOT NULL,
    Category VARCHAR(64) not null,
    Required_Age text not null,
    Popularity real not null,
    RAM INT not null,
    Processor_Speed INT not null,
    Graphics INT NOT NULL,
    Windows_Compatible INT not null,
    Linux_Compatible INT not null,
    Mac_Compatible INT not null,
    Game_Rating DECIMAL(5,2) GENERATED ALWAYS AS (
    (
        (Processor_Speed * 0.4) + (RAM * 0.3) + (Graphics * 0.3)
    ) 
    / 8.2 * 5
) VIRTUAL
);

## Team Table
CREATE TABLE Team (
    Team_Id varchar(64) PRIMARY KEY,
    Team_Name varchar(64) NOT NULL);

## Team to connect Users to Team
CREATE TABLE Team_to_User (
    Team_Id varchar(64) ,
    User_Id varchar(16) ,
    FOREIGN KEY (Team_Id) REFERENCES Team(Team_Id) ON DELETE SET NULL,
    FOREIGN KEY (User_Id) REFERENCES User(User_Id) ON DELETE SET NULL);
    
CREATE TABLE Matches (
    Match_ID varchar(64) PRIMARY KEY,
    Team1_ID varchar(64),
    Team2_ID varchar(64),
    Game_ID varchar(64) NOT NULL,
    Match_Date DATETIME NOT NULL,
    Match_Status ENUM('Scheduled', 'In Progress', 'Completed') NOT NULL,
    Winner_Team_ID varchar(64),
    FOREIGN KEY (Team1_ID) REFERENCES Team(Team_Id),
    FOREIGN KEY (Team2_ID) REFERENCES Team(Team_Id),
    FOREIGN KEY (Game_ID) REFERENCES Game(Game_Id)
);
