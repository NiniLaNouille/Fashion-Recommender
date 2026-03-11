from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def home():

    return """

    <h1>Fashion Recommender</h1>

    <p>Your weekly recommendations will appear here.</p>

    """
