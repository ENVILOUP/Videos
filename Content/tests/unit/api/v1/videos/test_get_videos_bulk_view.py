
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import UUID
from fastapi.testclient import TestClient
from app.api.v1.videos.dependencies import get_videos_by_uuid_list_use_case
from app.application.use_cases.get_videos_by_uuid_list import GetVideosByUUIDsListUseCase
from app.core.entities.video import Video
from app.main import app

client = TestClient(app)

class TestGetVideosBulkView:

    @staticmethod
    async def mock_get_videos_by_uuid_list_use_case():
        MockGetVideosByUUIDsListUseCase = Mock(spec=GetVideosByUUIDsListUseCase)
        MockGetVideosByUUIDsListUseCase.execute = AsyncMock(
            return_value=[
                Video(
                    video_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
                    title="Test Video 1",
                    description="Description for Test Video 1",
                    is_deleted=False,
                    created_at=datetime.fromisoformat("2025-01-01T00:00:00"),
                    modified_at=datetime.fromisoformat("2025-01-01T00:00:00"),
                ),
                Video(
                    video_uuid=UUID("123e4567-e89b-12d3-a456-426614174001"),
                    title="Test Video 2",
                    description="Description for Test Video 2",
                    is_deleted=True,
                    created_at=datetime.fromisoformat("2025-01-02T00:00:00"),
                    modified_at=datetime.fromisoformat("2025-01-02T00:00:00"),
                )
            ]
        )
        return MockGetVideosByUUIDsListUseCase
    
    @staticmethod
    def mock_get_videos_by_uuid_list_not_found_use_case():
        MockGetVideosByUUIDsListUseCase = Mock(spec=GetVideosByUUIDsListUseCase)
        MockGetVideosByUUIDsListUseCase.execute = AsyncMock(
            return_value=[]
        )
        return MockGetVideosByUUIDsListUseCase

    
    def test_happy_path(self):
        """
        Test the happy path for the get_videos_bulk endpoint.
        """
        video_uuids = [
            "123e4567-e89b-12d3-a456-426614174000",
            "123e4567-e89b-12d3-a456-426614174001"
        ]
        app.dependency_overrides[get_videos_by_uuid_list_use_case] = self.mock_get_videos_by_uuid_list_use_case

        response = client.post('api/v1/videos/get-bulk/', json=video_uuids)        
        
        assert response.status_code == 200
        assert response.json()["status_code"] == 1000
        assert response.json()["success"] is True
        assert response.json()["data"] == [
            {
                "video_uuid": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Test Video 1",
                "description": "Description for Test Video 1",
                "is_deleted": False,
                "created_at": "2025-01-01T00:00:00",
                "modified_at": "2025-01-01T00:00:00",
                "video_url": f'http://cdn.enviloup.localhost/videos/123e4567-e89b-12d3-a456-426614174000/master.m3u8',
                "thumbnail_url": f'http://cdn.enviloup.localhost/thumbnails/123e4567-e89b-12d3-a456-426614174000/default.webp',
                "publication_date": "2025-01-01T00:00:00",
            },
            {
                "video_uuid": "123e4567-e89b-12d3-a456-426614174001",
                "title": "Test Video 2",
                "description": "Description for Test Video 2",
                "is_deleted": True,
                "created_at": "2025-01-02T00:00:00",
                "modified_at": "2025-01-02T00:00:00",
                "video_url": f'http://cdn.enviloup.localhost/videos/123e4567-e89b-12d3-a456-426614174001/master.m3u8',
                "thumbnail_url": f'http://cdn.enviloup.localhost/thumbnails/123e4567-e89b-12d3-a456-426614174001/default.webp',
                "publication_date": "2025-01-02T00:00:00",
            }
        ]

    def test_not_found(self):
        """
        Test the not found case for the get_videos_bulk endpoint.
        """
        video_uuids = [
            "123e4567-e89b-12d3-a456-426614174000",
            "123e4567-e89b-12d3-a456-426614174001"
        ]
        app.dependency_overrides[get_videos_by_uuid_list_use_case] = self.mock_get_videos_by_uuid_list_not_found_use_case
        
        response = client.post("api/v1/videos/get-bulk/", json=video_uuids)
        
        assert response.status_code == 200
        assert response.json()["status_code"] == 1000
        assert response.json()["success"] is True
        assert response.json()["data"] == []

    def test_invalid_uuid(self):
        """
        Test the invalid UUID case for the get_videos_bulk endpoint.
        """
        video_uuids = [
            "123e4567-e89b-12d3-a456-426614174000",
            "invalid-uuid"
        ]
        app.dependency_overrides[get_videos_by_uuid_list_use_case] = MagicMock()
        
        response = client.post("api/v1/videos/get-bulk/", json=video_uuids)
        
        assert response.status_code == 422
        assert response.json()["success"] is False
        assert response.json()["status_code"] == 1001
