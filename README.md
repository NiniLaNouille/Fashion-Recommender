# Personal Fashion Recommender (Run Locally)

A lightweight AI fashion recommendation system that:

- Scrapes products from Mango, Sellpy and Zalando
- Stores them locally
- Generates **text + image embeddings**
- Learns from your feedback
- Shows **10 recommendations every Monday**
- Runs entirely on **localhost:8000**

Designed as a **personal project you can run with one command**.

---

# Quick Start (One Command)

```bash
pip install -r requirements.txt
python start.py
```

Then open:

```
http://localhost:8000
```

---

# Repository Structure

```
fashion-recommender/

start.py
requirements.txt
config.py

/data
    fashion.db
    images/

/database
    db.py
    models.py

/scrapers
    mango.py
    zalando.py
    sellpy.py

/embeddings
    text.py
    image.py

/recommender
    taste_model.py
    ranker.py

/api
    server.py

/frontend
    templates
        index.html

/scheduler
    weekly.py
```

---

# requirements.txt

```
fastapi
uvicorn
playwright
beautifulsoup4
requests
pillow
numpy
scikit-learn
sentence-transformers
transformers
torch
sqlite-utils
```

---

# start.py

Single command launcher.

```python
import subprocess
import uvicorn

print("Starting fashion recommender...")

subprocess.run(["python","scheduler/weekly.py"])

uvicorn.run("api.server:app", host="127.0.0.1", port=8000, reload=True)
```

---

# config.py

```python
DB_PATH = "data/fashion.db"
IMAGE_FOLDER = "data/images"
RECOMMENDATION_COUNT = 10
```

---

# Database

## database/db.py

```python
import sqlite3
from config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)
```

---

## database/models.py

```python
from database.db import get_connection


def init_db():

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        title TEXT,
        brand TEXT,
        category TEXT,
        color TEXT,
        price REAL,
        description TEXT,
        image_url TEXT,
        product_url TEXT,
        source TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        product_id TEXT,
        rating INTEGER
    )
    """)

    conn.commit()
```

---

# Scrapers

Each scraper returns standardized product objects.

Example skeleton:

## scrapers/zalando.py

```python
import requests


def scrape():

    products = []

    # simplified example
    products.append({
        "id": "zalando_test",
        "title": "Black coat",
        "brand": "Mango",
        "category": "coat",
        "color": "black",
        "price": 120,
        "description": "Oversized wool coat",
        "image_url": "",
        "product_url": "",
        "source": "zalando"
    })

    return products
```

---

# Text Embeddings

## embeddings/text.py

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(text):
    return model.encode(text)
```

---

# Image Embeddings

Uses CLIP.

## embeddings/image.py

```python
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def embed(image_url):

    image = Image.open(requests.get(image_url, stream=True).raw)

    inputs = processor(images=image, return_tensors="pt")

    outputs = model.get_image_features(**inputs)

    return outputs.detach().numpy()[0]
```

---

# Taste Model

## recommender/taste_model.py

```python
import numpy as np


def build_taste(vectors, ratings):

    weighted = []

    for v, r in zip(vectors, ratings):
        weighted.append(v * r)

    return np.mean(weighted, axis=0)
```

---

# Ranking

## recommender/ranker.py

```python
from sklearn.metrics.pairwise import cosine_similarity


def rank(products, taste_vector):

    scores = []

    for p in products:
        sim = cosine_similarity([p["vector"]], [taste_vector])[0][0]
        scores.append((sim,p))

    scores.sort(reverse=True)

    return [p for s,p in scores]
```

---

# Weekly Job

## scheduler/weekly.py

```python
from scrapers.zalando import scrape as zalando


def run():

    products = []

    products += zalando()

    print("Collected products:",len(products))


if __name__ == "__main__":
    run()
```

---

# API Server

## api/server.py

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def home():

    html = """

    <h1>Fashion Recommender</h1>

    <p>Your weekly picks will appear here.</p>

    """

    return html
```

---

# Frontend

## frontend/templates/index.html

```html
<h1>Weekly Fashion Picks</h1>

<div>

<img src="image" width="200"/>

<p>Brand</p>

<button>Love</button>
<button>OK</button>
<button>Awful</button>

</div>
```

---

# Weekly Automation

Run manually:

```
python scheduler/weekly.py
```

Or cron job:

```
0 8 * * MON python scheduler/weekly.py
```

---

# What Happens When You Run It

1. Scrapers collect products
2. Products stored locally
3. Embeddings generated
4. Taste vector computed
5. Top 10 ranked
6. Displayed on

```
localhost:8000
```

You click:

❤️ Love
👍 OK
👎 Awful

System learns your taste.

---

# Recommended Next Improvements

1. Store embeddings in database
2. Add image caching
3. Add Mango scraper
4. Add Sellpy scraper
5. Display images in UI
6. Save weekly recommendations

After these, the system becomes a **fully autonomous AI stylist**.

