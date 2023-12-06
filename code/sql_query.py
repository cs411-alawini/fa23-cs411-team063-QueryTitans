import sqlite3
from google.cloud import storage 
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import sys
from mysql.connector import pooling


# Query 1
def get_query_user_login_validation(user_id, password):
    return f"""SELECT * 
        FROM User 
        WHERE User_Id = "{user_id}" AND Pass_Word = "{password}";"""

# Query 2
# To-Do
def get_query_matches():
    return """Select * from Matches WHERE Match_Status='Scheduled';"""

# Query 3
def get_query_profile_details(user_id):
    return f"""SELECT * 
FROM User 
WHERE User_Id = "{user_id}";"""

# Query 4
def update_query_profile_details(user_id, first_name, last_name, email, preferred_genre, preferred_category):
    return f'''UPDATE User 
SET 
    First_Name = "{first_name}",
    Last_Name = "{last_name}",
    Email = "{email}",
    Preferred_Genre = "{preferred_genre}",
    Preferred_Category = "{preferred_category}"
WHERE 
    User_Id = "{user_id}"'''

# Query 5
def update_query_laptop_details(user_id, laptop_id):
    return f"""UPDATE User 
SET 
    Laptop_Id = "{laptop_id}"
WHERE 
    User_Id = "{user_id}";"""
    
# Query 6
def create_query_add_user(user_id, first_name, last_name, password, date_of_birth, email, preferred_genre, preferred_category, user_type, selected_laptop_id):
    return f"""INSERT INTO User (User_Id, First_Name, Last_Name, Pass_Word, Date_of_Birth, Email, Preferred_Genre, Preferred_Category, User_Type, Laptop_Id)
VALUES ('{user_id}', '{first_name}', '{last_name}', '{password}', '{date_of_birth}', '{email}', '{preferred_genre}', '{preferred_category}', '{user_type}', '{selected_laptop_id}');"""

# Query 7
def get_query_game_rec(user_id):
    return f"""SELECT distinct
    User.User_Id,
    Game.Game_Id, 
    Game.Game_Name, 
    Game.Price,
    Game.Category,
    Game.Genre,
    Game.Popularity
FROM 
    User
LEFT JOIN 
    Laptop ON User.Laptop_Id = Laptop.Laptop_Id
LEFT JOIN 
    Game ON User.Preferred_Genre = Game.Genre
WHERE 
    User.user_id = "{user_id}"
    AND Game.Game_Id IN (
        SELECT Game_Id FROM Game WHERE Game.Game_Rating < Laptop.Laptop_Rating
    )
    AND Game.Required_Age <= User.Age
    AND Game.Game_Rating <= Laptop.Laptop_Rating
    AND Game.Category=User.Preferred_Category
    order by Game.Popularity DESC;
    """

# Query 8
def get_query_search(search_term):
    return f"""SELECT 'Game' AS Type, Game_Id AS Id, Game_Name AS Name
FROM Game
WHERE Game_Name LIKE CONCAT('%', '{search_term}', '%')

UNION

SELECT 'User' AS Type, User_Id AS Id, CONCAT(First_Name, ' ', Last_Name) AS Name
FROM User
WHERE First_Name LIKE CONCAT('%', '{search_term}', '%') 
   OR Last_Name LIKE CONCAT('%', '{search_term}', '%');
"""

def validate_team_match(team_id, game_id, match_date):
    return f"call esports.RegisterTeamForMatchAndCreateOrUpdateMatch('{team_id}', '{game_id}', '{match_date}');"

def get_query_all_laptops():
    return f"SELECT * FROM Laptop"

def delete_query_laptop_from_user(user_id):
    return f"""UPDATE User
SET Laptop_Id = NULL
WHERE User_id = '{user_id}';"""

def update_query_register_new_team(team_id, team_name):
    return f"""INSERT INTO Team (Team_id, Team_Name) VALUES ('{team_id}', '{team_name}');"""

def update_query_add_user_to_existing_team(team_id, user_id):
    return f""" INSERT INTO Team_to_User (Team_Id, User_Id) VALUES ('{team_id}', '{user_id}');
    """

def get_query_game_rec_pop():
    return f"""SELECT distinct
    G1.Game_Id, 
    G1.Game_Name, 
    G1.Price,
    G1.Category,
    G1.Genre,
    G1.Popularity
FROM 
    Game G1
INNER JOIN (
    SELECT 
        Category, 
        AVG(Popularity) AS Avg_Popularity
    FROM 
        Game
    GROUP BY 
        Category
) AS G2
ON 
    G1.Category = G2.Category
WHERE 
    G1.Popularity > G2.Avg_Popularity
ORDER BY 
    G1.Category DESC, G1.Popularity DESC;
    """


def query_database(sql_query):
    cnx = mysql.connector.connect(
        user='root',
        password='titans1234',
        host='35.184.155.230', 
        database='esports')

    cursor = cnx.cursor(buffered=True)

    query_exec = cursor.execute(sql_query)
    cnx.commit()

    df = pd.DataFrame(cursor.fetchall())

    cursor.close()
    cnx.close()

    return df

def update_database(sql_query):
    cnx = mysql.connector.connect(
        user='root',
        password='titans1234',
        host='35.184.155.230', 
        database='esports')

    cursor = cnx.cursor(buffered=True)
    query_exec = cursor.execute(sql_query)
    cnx.commit()

    cursor.close()
    cnx.close()
    return "SUCCESS"

def procedure_call_database(sql_query):
    cnx = mysql.connector.connect(
        user='root',
        password='titans1234',
        host='35.184.155.230', 
        database='esports')

    #cursor = cnx.cursor()
    #query_exec = cursor.execute(sql_query)

    #cnx.close()
    #print(query_exec)

    cursor = cnx.cursor()
    cursor.execute(sql_query)  # Execute the stored procedure

    # Fetch results
    results = cursor.fetchall()

    cnx.close()

    return results



# Test this
# Add Existing User to page


