from fastapi import FastAPI
from app.db import init_db
from app.routers.trends import router as trends_router

app = FastAPI(title="Trendylizer API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Trendylizer API"}

# Initialize the database (creates tables if needed)
init_db()

# Mount our API routes
app.include_router(trends_router, prefix="/trends")


def main():
    read_root()
