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


            es_instance = await self.connector.get_instance()

            videos_index = "cdc.public.videos"
            videos_body = {
                "query": {
                    "match": {
                        "title": query
                    }
                },
                "size": size,
                "from": from_index,
                "track_total_hits": True
            }
            videos_results = await es_instance.search(index=videos_index, body=videos_body)

            tags_index = "cdc.public.videos_tags"
            tags_body = {
                "query": {
                    "match": {
                        "tag": query
                    }
                },
                "size": size,
                "from": from_index,
                "track_total_hits": True
            }
            tags_results = await es_instance.search(index=tags_index, body=tags_body)

            hits_without_duplication = set(self._extract_video_uuids(videos_results)).union(set(self._extract_video_uuids(tags_results)))
            hits = list(hits_without_duplication)

            total_hits = self._extract_total_hits(videos_results) + self._extract_total_hits(tags_results)
            total_pages = (total_hits + size - 1) // size

            return SearchResponseModel(
                page=page,
                total_pages=total_pages,
                results=hits[:size]
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
