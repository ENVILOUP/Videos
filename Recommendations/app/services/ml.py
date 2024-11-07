import random
from typing import List


async def get_recommendations_for_videos(count: int = 20) -> List[int]:
    return random.sample(range(1,1000), count)
