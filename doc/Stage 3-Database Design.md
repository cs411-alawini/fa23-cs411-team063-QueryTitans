# Database Design

The stage 3 of our 411 Project revolves around initial implementation of the backend of our project. Given that our project is two fold ( has the two components of game recommendations and match scheduling), the team decided to focused on the game recommendation aspect of the project.

Below can be seen the development, as of today, on the project with the focus on the recommendation model of the system.

## Database Tables on GCP

The system is planned to be hosted on the Google Cloud Platform.
Based on the same, a connection was established and a project was ceated accordingly. For the project we decide to create a DB named `esports`.
Connection to GCP and the Esports DB are highlighted below:


1(Insert Image)


As the focus was on game recommendation aspect of the project, the majority of the tables created were related to entities that would be involved in the same, these entities were the User, the User's Laptop and the Games.
Apart from this, we also started working on the match scheduling portion of the system by implementing the tables pertaining to user teams.

The list of implemented tables can be seen below:


2(Insert Image)







As per stage submission requirements, the three tables with at least 1000 rows can be seen below:


3(Insert Image)


## DDL Commands

```sql

```

We do feel the need to provided explaination for some of the attributes defined; mainly the Laptop and Game Ratings.
It can be seen that Laptop & Game Ratings are calculated in a similar manner. We have tried to utilize weighted averages assinged to the 3 more important aspects to run a game, that is, Processor Speed, RAM and GPU.
Using these ratings with a calculated normalization factor, we are able to standardise the Ratings both for Game as well as Laptop ( multiplication done by 5 to get a rating scale of 1-5).
The normalization factor is calculated using the maximum possible values of the above mentioned attributes using the weighted values. 

## Advanced Queries

As mentioned above, the focus was to handle the game recommendation part of our project for this stage, hence, the two advanced queries below deal with the same:

### Query 1

```sql

```

The above query is one of our key queries for game recommendations. The query joins the User and Laptop Table in order to get the Laptop Rating for each user, and then performs a join on the Game table based on the User Preferred Category (This field is just a user input on what category of games does the user like). Post this join, there is a comparison between the Game_Rating and the Laptop_Rating which helps us figue out what games can actually run on the User's Laptop. This is followed by a Age Check (in order to ensure that the user is old enough to be able to play that particular game), post which equality operator ensures that the games recommended are to the user preferances. 


### Query 2

```sql

```

While Query 1 focuses on specific user recommendations, Query 2 is more generic. This query helps us to get the games that have a popularity above the average for their respective categories, hence making them in-demand games in that particular categories.
This query would be used to display game recommendations based on categories which would basically be used potentially on the home page or when a user is casually scrolling thorugh the website. 

## Index Analysis

### Query 1

Default Index:


```sql

```

### Query 2

Default Index:


```sql

```
