![image](https://github.com/priyansh19csu225/chessLeaderboard-backend/assets/71059426/db6ba7e7-272c-446b-a7bd-85589c952bc4)


# Description
This is a fast API backend that fetches result of top 50 classical players on Lichess.org and fetch various useful data information from their API for a chess leaderboard dashboard. Made with python + fastapi + sqlalchemy + uvicorn + postgres db

# Installation and running the server

Create the project.

```bash
git clone https://github.com/priyansh19csu225/chessLeaderboard-backend.git
```

Access the project directory.

```bash
cd chessLeaderboard-backend
```

Create a virtual environment (recommended) 

```bash
python3 -m venv env
```

Change variables in the ```.env``` file according to your system

On windows run (different command to activate virtual environment in different systems)

```bash
env\Scripts\activate
```

Install dependencies in virtual environment using command

```bash
pip install -r requirements.txt
```

Run command to start the server

```bash
uvicorn main:app --reload
```

Go to this url to access swagger documentation <http://127.0.0.1:8000/docs>

# Methods Documentation

This document provides an overview of the methods present in the codebase.

---

## `async def get_top_players() -> list:`

### Description:
Fetches the top 50 players' data from the Lichess API for classical games.

### Parameters:
None

### Returns:
A list containing data for the top 50 players.

---

## `async def fetch_player_rating_history(username: str, db: Session) -> list:`

### Description:
Fetches the rating history for a specific player from the Lichess API. It checks if the latest data exists in the database , if exists returns it otherwise updates it if necessary.

### Parameters:
- `username` (str): The username of the player.
- `db` (Session): The SQLAlchemy session object to interact with the database.

### Returns:
A list containing the player's rating history.

---

## `def find_last_30_days_points(rating_history: list) -> list:`

### Description:
Helper function that helps to extract the player's rating points from the last 30 days' data optimized by using binary search to search only required fields.

### Parameters:
- `rating_history` (list): A list containing the player's rating history.

### Returns:
A list of rating points from the last 30 days.

---

## `def generate_ratings(rating_history) -> list:`

### Description:
Helper function to generates a list of ratings from the player's rating history from result retrieved by find_last_30_days_points.

### Parameters:
- `rating_history`: A list of tuples containing (year, month, day, rating).

### Returns:
A list of ratings over the last 30 days.

---

## `async def generate_50_players_ratings_csv(top_50_players, db) -> str:`

### Description:
Generates a CSV file containing the rating history of the top 50 players over the last 30 days.

### Parameters:
- `top_50_players`: Data for the top 50 players.
- `db` (Session): The SQLAlchemy session object to interact with the database.

### Returns:
A string containing the CSV content.

---

## `def save_or_update_record_in_db(db: Session, username: str, ratings: list, last_modified_date: datetime):`

### Description:
Saves or updates a player's rating history in the database.

### Parameters:
- `db` (Session): The SQLAlchemy session object to interact with the database.
- `username` (str): The username of the player.
- `ratings` (list): A list containing the player's rating history.
- `last_modified_date` (datetime): The date when the rating history was last modified.

### Returns:
None

---

# API Usage Documentation

This document details the available endpoints and their functionalities for the API running on `127.0.0.1`.

---

## **GET** `/top-players`

### Description
Fetches data for the top 50 classical players.

### Response
- **200 OK**:
  - Returns data for the top 50 players.

- **500 Internal Server Error**:
  - Failed to fetch players' data.

---

## **GET** `/player/{username}/rating-history`

### Description
Retrieves the rating history for a specific player for the last 30 days.

### Parameters
- `{username}` (str): The username of the player.

### Response
- **200 OK**:
  - Returns the rating history for the player.

- **404 Not Found**:
  - Player rating history for the last 30 days not found.

---

## **GET** `/players/rating-history-csv`

### Description
Generates a CSV file containing the rating history of the top 50 players for the last 30 days.

### Response
- **200 OK**:
  - Downloads a CSV file containing the rating history.

- **404 Not Found**:
  - Top 50 classical players not found.
  
### Note:
- The file will be downloaded with the name `rating_history.csv`.

---

### **Note:** 

All endpoints require the API to be running locally (`127.0.0.1`).

# Optimizations for Improved Performance

## 1. TTLCache for CSV Content

- Utilize TTLCache to store CSV content temporarily, reducing the need to regenerate the CSV file on every request within a specified time.

## 2. Database Query Optimization

- Optimize database queries by fetching only required data and avoiding unnecessary operations. This minimizes database load and speeds up response times.

## 3. Async/Await Pattern

- Leverage async/await functionality to handle concurrent API requests efficiently, allowing multiple requests to be processed concurrently.

## 4. Error Handling and Logging

- Implement robust error handling mechanisms to gracefully handle errors and log necessary details for debugging purposes.

## 5. Minimize Data Processing

- Streamline data processing by optimizing algorithms, avoiding unnecessary iterations, and using efficient data structures.

## 6. Indexing in the Database

- Ensure proper indexing on columns used for querying in the database. This enhances query performance, especially for large datasets.


## Documentation and Testing API

![image](https://github.com/priyansh19csu225/chessLeaderboard-backend/assets/71059426/c6f2268e-0100-4170-80a6-31e1e5d9e8d2)

![image](https://github.com/priyansh19csu225/chessLeaderboard-backend/assets/71059426/a38f36ba-f544-46bc-a13f-c773fc7731d1)

![image](https://github.com/priyansh19csu225/chessLeaderboard-backend/assets/71059426/daf7f056-be55-4237-a8a2-8f40925bb80d)

![image](https://github.com/priyansh19csu225/chessLeaderboard-backend/assets/71059426/c6270014-6cc5-43ad-b60c-d0cdfcc3bbfe)

![image](https://github.com/priyansh19csu225/chessLeaderboard-backend/assets/71059426/316dde35-f56b-49ba-8d44-cc537525b4d5)

![image](https://github.com/priyansh19csu225/chessLeaderboard-backend/assets/71059426/8c8fb9c5-bbf1-40f9-ab23-dd7f6e230adf)

![image](https://github.com/priyansh19csu225/chessLeaderboard-backend/assets/71059426/3e273175-3c29-42a9-8f3c-5564eb25db63)






