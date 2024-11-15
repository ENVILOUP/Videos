from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(
    root_path="/search"
)

es = Elasticsearch("http://localhost:9200")

@app.post("/")
async def search(client_query: str):
    query_json = {
        "query": {
            "fuzzy": {
                "title": {
                    "value": client_query.casefold(),
                    "fuzziness": 20,
                    "transpositions": True
                }
            }
        }
    }

    response = es.search(index="videos", body=query_json)

    hits_list = []

    for hit in response['hits']['hits']:
        hits_list.append(hit['_source'])

    return hits_list 