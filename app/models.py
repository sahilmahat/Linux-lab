from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    saved_issues = relationship("SavedIssue", back_populates="owner")
    search_history = relationship("SearchHistory", back_populates="user")


class SavedIssue(Base):
    __tablename__ = "saved_issues"

    id = Column(Integer, primary_key=True, index=True)
    issue_key = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    saved_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="saved_issues")


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    issue_key = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    searched_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="search_history")
