from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    genre_id = Column(Integer)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=True)


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title: str = Column(String)
    original_title = Column(String)
    release_year = Column(Integer)
    source: str = Column(String)
    rating: str = Column(String)
    created_datetime = Column(DateTime, default=datetime.utcnow)

    genres = relationship('Genre', cascade="all", backref="movie", lazy=True)
