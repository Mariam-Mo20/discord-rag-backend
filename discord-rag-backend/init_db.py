from database import Base, engine
from models import Feedback, QuestionAnswer

Base.metadata.create_all(bind=engine)
