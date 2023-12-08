from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PlayerRatingHistory(Base):
    __tablename__ = 'players_rating_history'

    username = Column(String, primary_key=True)
    rating_history = Column(JSON)
    last_modified_date = Column(DateTime, nullable=False)

    def __init__(self, username, rating_history, last_modified_date):
        self.username = username
        self.rating_history = rating_history
        self.last_modified_date = last_modified_date
        
def create_table(engine):
    Base.metadata.create_all(bind=engine)