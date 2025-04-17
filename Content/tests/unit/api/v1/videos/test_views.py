
from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import UUID
from fastapi.testclient import TestClient
from app.api.v1.videos.dependencies import get_video_by_uuid_use_case
from app.application.use_cases.get_video_by_uuid import GetVideoByUUIDUseCase
from app.core.entities.video import Video
from app.core.ports.get_video_by_uuid import GetVideoByUUIDPort
from app.main import app

client = TestClient(app)


class TestVideosViewsV1:

    @staticmethod
    async def mock_get_video_by_uuid_use_case() -> GetVideoByUUIDUseCase:
        MockGetVideoByUUIDPort = Mock(spec=GetVideoByUUIDPort)
        MockGetVideoByUUIDPort.get_video_by_uuid = AsyncMock(
            return_value=Video(
                video_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
                yt_id="abcd1234",
                title="Test Video",
                description="This is a test video.",
                created_at=datetime.now(),
                modified_at=datetime.now(),
                is_deleted=False
            )
        )
        return GetVideoByUUIDUseCase(
            get_video_by_uuid=MockGetVideoByUUIDPort
        )


    def test_get_video_by_uuid(self):
        """
        Test the retrieval of a video by its UUID.
        """
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
        app.dependency_overrides[get_video_by_uuid_use_case] = self.mock_get_video_by_uuid_use_case

        response = client.get(f"/api/v1/videos/{valid_uuid}")
        
        assert response.status_code == 200
        assert response.json()["status_code"] == 1000
        assert "data" in response.json()
        assert response.json()["data"]["video_uuid"] == valid_uuid

        app.dependency_overrides.clear()




