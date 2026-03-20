from database.models import init_db
from recommender.pipeline import run_weekly_pipeline
import uvicorn

# Initialize DB and run weekly pipeline
init_db()
run_weekly_pipeline()

# This is the fix for Windows multiprocessing
if __name__ == "__main__":
    uvicorn.run("api.server:app", host="127.0.0.1", port=8000, reload=True)
