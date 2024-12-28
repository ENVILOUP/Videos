from fastapi import FastAPI, Query
import random
import config

app = FastAPI(
    root_path="/search"
)


@app.post("/find")
async def search(page: int = Query(1, ge=1), size: int = Query(10, gt=0), query: str = Query("")):

    start_index = (page - 1) * size
    end_index = start_index + size
    paginated_ids = config.enviloup_ids[start_index:end_index]

    random_ids = random.sample(paginated_ids, size-1)

    return random_ids 