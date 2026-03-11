import uvicorn
from database.models import init_db
from scheduler.weekly import run

print("Initializing database...")
init_db()

print("Running weekly pipeline...")
run()

print("Starting server...")

uvicorn.run("api.server:app", host="127.0.0.1", port=8000, reload=True)
