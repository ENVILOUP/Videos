import logging
from typing import List, Optional
from app.dependencies.elasticsearch import ElasticConnector

logger = logging.getLogger('uvicorn.error')


class SearchService:
    def __init__(self, connector: ElasticConnector):
        self.connector = connector

    async def search_videos(self, query: str, page: int, size: int) -> dict:
        try:
            start_index = (page - 1) * size
            end_index = start_index + size

            results = await self.connector._es.search(
                index="cdc.public.videos",
                body={
                    "query": {
                        "match": {
                            "title": {
                                "query": query,
                                "fuzziness": "auto"
                            }
                        }
                    }
                }
            )

            hits = self._extract_video_uuids(results)
            total_hits = len(hits)
            total_pages = (total_hits + size - 1) // size

            paginated_ids = hits[start_index:end_index]

            return {
                "page": page,
                "total_pages": total_pages,
                "results": paginated_ids
            }

        except Exception as e:
            logger.error(f"Error during search: {e}", exc_info=True)
            raise

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
