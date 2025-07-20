from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging
import time
import models
from database import SessionLocal, engine
from models import QuestionAnswer, Feedback
from rag import get_answer_from_rag

# Metrics tracking variables
metrics = {
    "total_requests": 0,
    "errors": 0,
    "latencies": []
}

# Create tables
models.Base.metadata.create_all(bind=engine)

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Database dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Models
class QueryRequest(BaseModel):
    user_id: str
    question: str

class FeedbackRequest(BaseModel):
    user_id: str
    question: str
    answer: str
    rating: int
    comment: str = None

# Root route to confirm backend is working
@app.get("/")
def read_root():
    return {"message": "Hello,Backend is working 🎉"}

# Route to return simple metrics
@app.get("/metrics")
def read_metrics():
    total = metrics["total_requests"]
    errors = metrics["errors"]
    avg_latency = round(sum(metrics["latencies"]) / total, 2) if total > 0 else 0
    return {
        "total_requests": total,
        "errors": errors,
        "average_latency_sec": avg_latency
    }

# RAG query route
@app.post("/api/rag-query")
async def rag_query(request: Request, db: Session = Depends(get_db)):
    total_start = time.time()  # Start total timer

    body = await request.json()
    logger.info(f"[DEBUG] Raw body: {body}")

    try:
        data = QueryRequest(**body)
        logger.info(f"[QUERY] From user: {data.user_id} | Question: {data.question}")

        # RAG processing time
        rag_start = time.time()
        answer = get_answer_from_rag(data.question)
        rag_duration = time.time() - rag_start
        logger.info(f"[TIMER] RAG time: {rag_duration:.2f} sec")

        # Save result to DB
        db_start = time.time()
        qa = QuestionAnswer(
            user_id=data.user_id,
            question=data.question,
            answer=answer
        )
        db.add(qa)
        db.commit()
        db.refresh(qa)
        db_duration = time.time() - db_start
        logger.info(f"[TIMER] DB time: {db_duration:.2f} sec")

    except Exception as e:
        logger.error(f"[ERROR] {str(e)}")
        answer = "Sorry, I couldn't get an answer right now."
        metrics["errors"] += 1

    total_duration = time.time() - total_start
    metrics["total_requests"] += 1
    metrics["latencies"].append(total_duration)
    logger.info(f"[TIMER] Total time: {total_duration:.2f} sec")

    return {
        "user_id": body.get("user_id", "unknown"),
        "answer": answer
    }

# Feedback submission route
@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    logger.info(f"[FEEDBACK] From user: {feedback.user_id} | Rating: {feedback.rating} | Comment: {feedback.comment}")

    try:
        fb = Feedback(
            user_id=feedback.user_id,
            question=feedback.question,
            answer=feedback.answer,
            rating=feedback.rating,
            comment=feedback.comment
        )
        db.add(fb)
        db.commit()
        db.refresh(fb)

        return {
            "message": "Feedback saved successfully",
            "data": feedback
        }

    except Exception as e:
        db.rollback()
        metrics["errors"] += 1
        logger.error(f"Database error: {str(e)}")
        return {"error": "Could not save feedback"}
