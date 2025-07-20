from database import SessionLocal
from models import Feedback

db = SessionLocal()

feedbacks = db.query(Feedback).all()

for fb in feedbacks:
    print(f"User: {fb.user_id} | Rating: {fb.rating} | Q: {fb.question} | Comment: {fb.comment}")
