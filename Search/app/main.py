from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch

app = FastAPI(
    root_path="/search"
)

es = Elasticsearch("http://elasticsearch:9200")

@app.post("/")
async def search(client_query: str):
    query_json = {
            "query": {
                "match": {
                    "title": {
                        "query": client_query.lower(),
                        "fuzziness": "2"
                    }
                }
            }
    }

    response = es.search(index="video", body=query_json)

    hits_list = []

    for hit in response['hits']['hits']:
        hits_list.append(hit['_source'])

    return hits_list 