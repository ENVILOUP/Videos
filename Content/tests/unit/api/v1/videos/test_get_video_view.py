
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import UUID
from fastapi.testclient import TestClient
from app.api.v1.videos.dependencies import get_video_by_uuid_use_case
from app.application.use_cases.get_video_by_uuid import GetVideoByUUIDUseCase
from app.core.entities.video import Video
from app.core.ports.get_video_by_uuid import GetVideoByUUIDPort
from app.infrastructure.entrypoints.fastapi import app

client = TestClient(app)


class TestGetVideoView:

    @staticmethod
    async def mock_get_video_by_uuid_use_case() -> GetVideoByUUIDUseCase:
        MockGetVideoByUUIDPort = Mock(spec=GetVideoByUUIDPort)
        MockGetVideoByUUIDPort.get_video_by_uuid = AsyncMock(
            return_value=Video(
                video_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
                yt_id="abcd1234",
                title="Test Video",
                description="This is a test video.",
                created_at=datetime.fromisoformat("2025-01-01T00:00:00"),
                modified_at=datetime.fromisoformat("2025-01-01T00:00:00"),
                is_deleted=False
            )
        )
        return GetVideoByUUIDUseCase(
            get_video_by_uuid=MockGetVideoByUUIDPort
        )

    @staticmethod
    async def mock_get_video_by_uuid_use_case_not_found() -> GetVideoByUUIDUseCase:
        MockGetVideoByUUIDPort = Mock(spec=GetVideoByUUIDPort)
        MockGetVideoByUUIDPort.get_video_by_uuid = AsyncMock(return_value=None)
        return GetVideoByUUIDUseCase(
            get_video_by_uuid=MockGetVideoByUUIDPort
        )

    def test_happy_path(self):
        """
        Test the retrieval of a video by its UUID.
        """
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
        app.dependency_overrides[get_video_by_uuid_use_case] = self.mock_get_video_by_uuid_use_case

        response = client.get(f"/api/v1/videos/{valid_uuid}")
        
        assert response.status_code == 200
        assert response.json()["status_code"] == 1000
        assert response.json()["success"] == True
        assert "data" in response.json()
        assert response.json()["data"] == {
            "video_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Test Video",
            "description": "This is a test video.",
            "is_deleted": False,
            "created_at": '2025-01-01T00:00:00',
            "modified_at": '2025-01-01T00:00:00',
            "video_url": "http://cdn.enviloup.localhost/videos/123e4567-e89b-12d3-a456-426614174000/master.m3u8",
            "thumbnail_url": "http://cdn.enviloup.localhost/thumbnails/123e4567-e89b-12d3-a456-426614174000/default.webp",
            "publication_date": '2025-01-01T00:00:00'
        }

        app.dependency_overrides.clear()
    
    def test_not_found(self):
        """
        Test the retrieval of a video by UUID that does not exist.
        """
        not_found_uuid = "123e4567-e89b-12d3-a456-426614174000"
        app.dependency_overrides[get_video_by_uuid_use_case] = self.mock_get_video_by_uuid_use_case_not_found

        response = client.get(f"/api/v1/videos/{not_found_uuid}")
        
        assert response.status_code == 404
        assert response.json()["success"] == False
        assert response.json()["status_code"] == 1002

        app.dependency_overrides.clear()
    
    def test_invalid_uuid(self):
        """
        Test the retrieval of a video by an invalid UUID.
        """
        invalid_uuid = "invalid-uuid"

        app.dependency_overrides[get_video_by_uuid_use_case] = MagicMock()
        
        response = client.get(f"/api/v1/videos/{invalid_uuid}")
        
        assert response.status_code == 422
        assert response.json()["success"] == False
        assert response.json()["status_code"] == 1001
