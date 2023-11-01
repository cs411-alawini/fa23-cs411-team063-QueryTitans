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

## Advanced Queries

### Query 1

```sql

```


### Query 2

```sql

```



## Index Analysis

### Query 1

Default Index:


```sql

```

### Query 2

Default Index:


```sql

```
