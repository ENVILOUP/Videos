from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    root_path="/search"
)


@app.post("/")
async def search(client_query: str):

    hits_list = []

    for hit in response['hits']['hits']:
        hits_list.append(hit['_source'])

    return hits_list 