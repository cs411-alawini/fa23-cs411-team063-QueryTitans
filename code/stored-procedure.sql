DELIMITER //

CREATE PROCEDURE RegisterTeamForMatchAndCreateOrUpdateMatch(
    IN input_team_id VARCHAR(64), 
    IN input_game_id VARCHAR(64),
    IN match_date DATETIME
)
proc_label: BEGIN  -- Adding a label here
    DECLARE team_exists INT;
    DECLARE game_age_requirement VARCHAR(64);
    DECLARE numeric_game_age_requirement INT;
    DECLARE game_type VARCHAR(64);
    DECLARE single_member_age INT DEFAULT 0;
    DECLARE single_member_id VARCHAR(16);
    DECLARE single_member_name VARCHAR(128);
    DECLARE member_count INT;
    DECLARE finished INT DEFAULT 0;
    DECLARE existing_match_id VARCHAR(64);

    -- Cursor declaration
    DECLARE age_cursor CURSOR FOR 
        SELECT User.Age, User.User_Id, CONCAT(User.First_Name, ' ', User.Last_Name) 
        FROM User 
        JOIN Team_to_User ON User.User_Id = Team_to_User.User_Id
        WHERE Team_to_User.Team_Id = input_team_id;

    -- Handler for cursor completion
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

    -- Check if the team exists
    SELECT COUNT(*) INTO team_exists
    FROM Team
    WHERE Team_Id = input_team_id;

    IF team_exists = 0 THEN
        SELECT CONCAT('Team with ID ', input_team_id, ' not found. Please check if input correct or if team exists.') AS Error;
        LEAVE proc_label;  -- Exiting the procedure
    END IF;

    -- Fetch the age requirement and type for the game
    SELECT Required_Age, Category INTO game_age_requirement, game_type
    FROM Game
    WHERE Game_Id = input_game_id;

    -- Convert the age requirement to numeric if it's not 'All Ages'
    SET numeric_game_age_requirement = IF(game_age_requirement = 'All Ages', 0, CAST(SUBSTRING_INDEX(game_age_requirement, '+', 1) AS UNSIGNED));

    -- Count the number of team members
    SELECT COUNT(*) INTO member_count
    FROM Team_to_User
    WHERE Team_Id = input_team_id;

    -- Singleplayer game check
    IF game_type = 'SinglePlayer' THEN
        IF member_count != 1 THEN
            SELECT 'Singleplayer games require exactly one team member. Current Team has more than one team member. Kindly create new team to enter' AS Error;
            LEAVE proc_label;  -- Exiting the procedure
        ELSE
            -- Fetch the age of the single team member
            SELECT Age INTO single_member_age
            FROM User 
            JOIN Team_to_User ON User.User_Id = Team_to_User.User_Id
            WHERE Team_to_User.Team_Id = input_team_id;

            -- Single player age requirement check
            IF game_age_requirement != 'All Ages' AND single_member_age < numeric_game_age_requirement THEN
                SELECT 'The team member does not meet the age requirement for this game.' AS Error;
                LEAVE proc_label;  -- Exiting the procedure
            END IF;
        END IF;
    ELSE
        -- Multiplayer game check
        OPEN age_cursor;

        age_check_loop: LOOP
            FETCH age_cursor INTO single_member_age, single_member_id, single_member_name;
            
            IF finished THEN 
                CLOSE age_cursor;
                LEAVE age_check_loop;
            END IF;

            IF game_age_requirement != 'All Ages' AND single_member_age < numeric_game_age_requirement THEN
                SELECT CONCAT('Team member ', single_member_name, ' (', single_member_id, ') does not meet the age requirement for this game.') AS Error;
                CLOSE age_cursor;
                LEAVE proc_label;  -- Exiting the procedure
            END IF;
        END LOOP age_check_loop;
    END IF;

    -- Check for existing match with a free slot for the specified game
    SELECT Match_ID INTO existing_match_id
    FROM Matches
    WHERE Game_ID = input_game_id AND Team1_ID IS NOT NULL AND Team2_ID IS NULL
    LIMIT 1;

    -- If an existing match is found, update it with Team2_ID
    IF existing_match_id IS NOT NULL THEN
        UPDATE Matches
        SET Team2_ID = input_team_id
        WHERE Match_ID = existing_match_id;
        IF ROW_COUNT() > 0 THEN
            SELECT 'Team added to existing match.' AS Success;
        ELSE
            SELECT 'No match was updated. Please check the match details.' AS Error;
        END IF;
    ELSE
        -- If no existing match is found, insert a new match
        INSERT INTO Matches (Match_ID, Team1_ID, Game_ID, Match_Date, Match_Status)
        VALUES (
            UUID(),  -- Assuming Match_ID is a UUID
            input_team_id, 
            input_game_id, 
            match_date, 
            'Scheduled'  -- Default status, can be adjusted based on current time and match_date
        );
        SELECT 'New match successfully created.' AS Success;
    END IF;
END;

//

DELIMITER ;\