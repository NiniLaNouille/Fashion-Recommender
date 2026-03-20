from database.models import init_db
from recommender.pipeline import run_weekly_pipeline
import uvicorn


def main():
    print("Initializing database...")
    init_db()

    print("Running weekly pipeline...")
    run_weekly_pipeline()

    print("Starting server...")
    uvicorn.run("api.server:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
