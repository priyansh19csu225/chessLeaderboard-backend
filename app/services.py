from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import PlayerRatingHistory
import httpx

async def get_top_players() -> list:
    url = "https://lichess.org/api/player/top/50/classical"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()


async def fetch_player_rating_history(username: str, db: Session) -> list:
    # Get today's date at midnight
    today_midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Check if the user exists in the database
    db_user = db.query(PlayerRatingHistory).filter(PlayerRatingHistory.username == username).first()
    flag = db_user and db_user.last_modified_date.date() == today_midnight.date()
    if flag:
        return db_user.rating_history
    else:
        url = f"https://lichess.org/api/user/{username}/rating-history"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                desired_object = next((obj for obj in data if obj.get("name") == "Classical"), None)
                if desired_object:
                    last_30_days_points = find_last_30_days_points(desired_object["points"])
                    ratings = generate_ratings(last_30_days_points)
                    save_or_update_record_in_db(db,username,ratings,today_midnight)
                    return ratings
                else:
                    return []
            else:
                return []

def find_last_30_days_points(rating_history: list) -> list:
    thirty_days_ago = datetime.now() - timedelta(days=30)
    last_30_records = rating_history[-30:]
   
    left, right = 0, len(last_30_records) - 1
    closest_index = -1
    
    while left <= right:
        mid = (left + right) // 2
        date = datetime(last_30_records[mid][0], last_30_records[mid][1] + 1, last_30_records[mid][2])
        
        if date >= thirty_days_ago:
            right = mid - 1
        else:
            closest_index = mid
            left = mid + 1
    
    if closest_index == -1:
        return rating_history
    
    return last_30_records[closest_index:]

def generate_ratings(rating_history):
    """
    Generates a list of ratings from rating history.

    Args:
        rating_history: A list of tuples containing (year, month, day, rating).

    Returns:
        A list of ratings.
    """

    date_to_rating = {}
    previous_rating = rating_history[0][3]

    for year, month, date, rating in rating_history:
        one_indexed_date = (year, month + 1, date)
        date_to_rating[one_indexed_date] = rating

    # Get current date and calculate date 30 days ago
    current_date = datetime.now()
    thirty_days_ago = current_date - timedelta(days=30)

    ratings = []
    for i in range(30):
        target_date = thirty_days_ago + timedelta(days=i)
        target_date_tuple = (target_date.year, target_date.month, target_date.day)
        rating = date_to_rating.get(target_date_tuple)

        if rating is None:
            # Use previous rating if available
            rating = previous_rating
        else:
            # Update previous rating
            previous_rating = rating

        ratings.append(rating)

    return ratings

async def generate_50_players_ratings_csv(top_50_players,db):
     # Calculate starting date (30 days ago)
    start_date = datetime.today() - timedelta(days=30)

    # Generate date list for header
    dates = [start_date + timedelta(days=i) for i in range(30)]

    # Generate header
    header = ["Username"] + ["Rating on {}".format(date.strftime("%Y-%m-%d")) for date in dates]
    rows = [header]
    
    for player in top_50_players["users"]:
        username = player["username"]
        row = await fetch_player_rating_history(username,db)
        firstColumn = [username]        
        rows.append(list(firstColumn)+row)
    
    # Generate CSV content and set response headers
    csv_content = "\n".join([",".join(map(str, row)) for row in rows])
    return csv_content

def save_or_update_record_in_db(db: Session, username: str, ratings: list, last_modified_date: datetime):
    # Check if the user exists in the database
    db_user = db.query(PlayerRatingHistory).filter(PlayerRatingHistory.username == username).first()
    
    if db_user:
        # If the user exists, update the existing record
        db_user.rating_history = ratings
        db_user.last_modified_date = last_modified_date
    else:
        # If the user doesn't exist, create a new record
        db_user = PlayerRatingHistory(username=username, rating_history=ratings, last_modified_date=last_modified_date)
        db.add(db_user)
    
    db.commit()
    db.refresh(db_user)
