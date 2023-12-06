import sqlite3
from google.cloud import storage 
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import sys

#### Establish Connetion ####

def main():
    cnx = mysql.connector.connect(
        user='root',
        password='titans1234',
        host='35.184.155.230',
        database='esports')
    cursor = cnx.cursor(buffered=True)

    user_id = "Uid1"
    password = "pD6,?p$7Ps5{+"

    query_count = "select count(*) from Game;"

    query_login = f"""SELECT * 
    FROM User 
    WHERE User_Id = "{user_id}" AND Pass_Word = "{password}";"""

    query_update_profile_details = f"""UPDATE User 
    SET 
        First_Name = "Mark",
        Last_Name = "Man",
        Date_of_Birth = STR_TO_DATE('07-25-2012','%m-%d-%Y'),
        Email = "hamp@gmail.com",
        Preferred_Genre = "Adventure",
        Preferred_Category = "VRSupport",
        User_Type = "Individual",
        Laptop_Id = "LP180" 
    WHERE 
        User_Id = "Uid1";
    """


    query1 = cursor.execute(query_login)
    cnx.commit()

    frame = pd.DataFrame(cursor.fetchall())
    print(frame)

    cursor.close()
    cnx.close()

if __name__ == '__main__':
    main()
