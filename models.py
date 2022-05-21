
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey

from sqlalchemy.orm import relationship

from database import Base





class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    hashed_password = Column(String(128))

    posts = relationship("Post", back_populates="author") # backpop -> Post.author



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    title = Column(String(255))
    body = Column(String(1024))
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts") # backpop -> User.items

    
