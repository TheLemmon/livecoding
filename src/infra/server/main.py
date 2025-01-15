import asyncio
from typing import Optional

import httpx
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/jokes/random", status_code=200)
def get_random_jokes(
    random_api_joke="https://api.chucknorris.io/jokes/random",
    category: Optional[str] = None,
):
    payload = {} if category is None else {"category": category}
    request = requests.get(random_api_joke, params=payload)
    return request.json()


@app.get("/api/jokes/categories", status_code=200)
def get_all_categories(categories_api="https://api.chucknorris.io/jokes/categories"):
    request = requests.get(categories_api)
    return request.json()


@app.get("/api/jokes/search", status_code=200)
def search_joke(query: str, search_api="https://api.chucknorris.io/jokes/search"):
    payload = {} if query is None else {"query": query}
    request = requests.get(search_api, params=payload)
    return request.json


class Joke(BaseModel):
    id: str
    url: str
    value: str


joke_api = "https://api.chucknorris.io/jokes/random"


async def get_multiples_jokes(chunk_size: int = 10) -> list[Joke]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(joke_api) for i in range(chunk_size)]
        responses = await asyncio.gather(*tasks)

        return [
            Joke(
                id=response.json()["id"],
                url=response.json()["url"],
                value=response.json()["value"],
            )
            for response in responses
        ]


@app.get("/api/jokes", response_model=list[Joke])
async def get_jokes():
    jokes: list[Joke] = []
    viewed_ids = {}

    while len(jokes) < 25:
        chuck_size = 25 - len(jokes)
        results = await get_multiples_jokes(chunk_size=chuck_size)
        for result in results:
            is_id_added = viewed_ids.get(result.id, False)
            if not is_id_added:
                viewed_ids[result.id] = True
                jokes.append(result)

    return jokes
