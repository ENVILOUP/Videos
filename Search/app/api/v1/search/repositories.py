import logging
from typing import List
from app.dependencies.elasticsearch import ElasticConnector

from app.api.v1.search.shemas import SearchResponseModel

logger = logging.getLogger('uvicorn.error')


class SearchRepository:
    def __init__(self, connector: ElasticConnector):
        self.connector = connector

    async def search_videos(self, query: str, page: int, size: int) -> SearchResponseModel:
        try:
            from_index = (page - 1) * size

            index = "cdc.public.videos"
            body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "tags"],
                        "fuzziness": "auto"
                    }
                },
                "size": size,
                "from": from_index
            }

            es_instance = await self.connector.get_instance()

            results = await es_instance.search(index=index, body=body)

            hits = self._extract_video_uuids(results)
            total_hits = self._extract_total_hits(results)
            total_pages = (total_hits + size - 1) // size

            return SearchResponseModel(
                page=page,
                total_pages=total_pages,
                results=hits
            )
        except Exception as e:
            logger.error(f"Error during search: {e}", exc_info=True)
            raise e

    def _extract_video_uuids(self, results: dict) -> List[str]:
        video_uuids = []
        for hit in results.get('hits', {}).get('hits', []):
            source = hit.get('_source', {})
            video_uuid = source.get('video_uuid')
            if video_uuid:
                video_uuids.append(video_uuid)
            else:
                logger.warning(f"Missing 'video_uuid' in search result: {hit}")
        return video_uuids

    def _extract_total_hits(self, results: dict) -> int:
        total_hits = 0
        total_hits = results.get('hits', {}).get('total', {}).get('value')
        if not total_hits:
            logger.warning(f"Missing 'total' in search result")
        return total_hits
