from fastapi import FastAPI, HTTPException
from utils.db import SessionLocal, TrendScore
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/trends")
def get_trends():
    session = SessionLocal()
    scores = session.query(TrendScore).order_by(TrendScore.score.desc()).limit(20).all()
    session.close()
    return [{"trend_name": t.trend_name, "score": t.score} for t in scores]

@app.get("/health")
def health_check():
    return {"status": "ok"}


def main():
    get_trends()
