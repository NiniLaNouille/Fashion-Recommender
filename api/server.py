from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scrapers.zalando import scrape

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():

    products = scrape()[:10]

    html = "<h1>Weekly Fashion Picks</h1>"

    for p in products:

        html += f"""
        <div style='margin-bottom:30px'>
            <img src='{p["image_url"]}' width='200'/>
            <p><b>{p["brand"]}</b></p>
            <p>{p["title"]}</p>
            <p>{p["price"]}€</p>
        </div>
        """

    return html
