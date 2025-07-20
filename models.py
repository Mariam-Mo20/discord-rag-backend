from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base


class QuestionAnswer(Base):
    __tablename__ = "qa_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    question = Column(String)
    answer = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    question = Column(Text)
    answer = Column(Text)
    rating = Column(Integer)
    comment = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
