from fastapi import FastAPI
from pydantic import BaseModel

from app.views import router as search_router
from app.config import config

app = FastAPI(
    title="Search Service",
    debug=config.debug
)

class BaseMessage(BaseModel):
    status: int
    message: str

@app.get("/")
async def health_check():
    return BaseMessage(status=200, message="Ok") 

app.include_router(search_router, prefix="")