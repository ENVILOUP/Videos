import random
from app.services.ml import VIDEOS_UUIDS


class RedisVideosRecommendation:
    def __init__(self, redis_client):
        self.redis_client = redis_client
    
    async def get_random_recommendations(self, size: int):
        return random.sample(VIDEOS_UUIDS, size)
