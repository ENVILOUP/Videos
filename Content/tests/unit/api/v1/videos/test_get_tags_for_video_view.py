from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, Mock
from fastapi.testclient import TestClient
from app.api.v1.videos.dependencies import get_tags_by_video_uuid_use_case
from app.application.use_cases.get_tags_by_video_uuid import GetTagsByVideoUUIDUseCase
from app.core.entities.tag import Tag
from app.core.ports.get_tags_by_video_uuid import GetTagsByVideoUUIDPort
from app.infrastructure.entrypoints.fastapi import app

client = TestClient(app)


class TestGetTagsForVideoView:

    @staticmethod
    async def mock_get_tags_by_video_uuid_use_case() -> GetTagsByVideoUUIDUseCase:
        MockGetTagsByVideoUUIDPort = Mock(spec=GetTagsByVideoUUIDPort)
        MockGetTagsByVideoUUIDPort.get_tags_by_video_uuid = AsyncMock(
            return_value=[
                Tag(
                    tag='foo',
                    created_at=datetime.fromisoformat('2025-01-01T00:00:00'),
                    modified_at=datetime.fromisoformat('2025-01-01T00:00:00')
                ),
                Tag(
                    tag='bar',
                    created_at=datetime.fromisoformat('2025-01-02T00:00:00'),
                    modified_at=datetime.fromisoformat('2025-01-02T00:00:00')
                )
            ]
        )
        return GetTagsByVideoUUIDUseCase(
            get_video_tags_by_video_uuid=MockGetTagsByVideoUUIDPort
        )
    
    @staticmethod
    async def mock_get_tags_by_video_uuid_use_case_not_found() -> GetTagsByVideoUUIDUseCase:
        MockGetTagsByVideoUUIDPort = Mock(spec=GetTagsByVideoUUIDPort)
        MockGetTagsByVideoUUIDPort.get_tags_by_video_uuid = AsyncMock(return_value=[])
        return GetTagsByVideoUUIDUseCase(
            get_video_tags_by_video_uuid=MockGetTagsByVideoUUIDPort
        )

    def test_happy_path(self):
        """
        Test the happy path for getting tags for a video.
        """
        app.dependency_overrides[get_tags_by_video_uuid_use_case] = self.mock_get_tags_by_video_uuid_use_case
        video_uuid = "123e4567-e89b-12d3-a456-426614174000"

        response = client.get(f"/api/v1/videos/{video_uuid}/tags")

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['status_code'] == 1000
        assert response.json()['data'] == ['foo', 'bar']

        app.dependency_overrides.clear()

    def test_not_found(self):
        """
        Test the case when no tags are found for a video.
        """
        video_uuid = "123e4567-e89b-12d3-a456-426614174000"
        app.dependency_overrides[get_tags_by_video_uuid_use_case] = self.mock_get_tags_by_video_uuid_use_case_not_found

        response = client.get(f"/api/v1/videos/{video_uuid}/tags")
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['status_code'] == 1000
        assert response.json()['data'] == []

        app.dependency_overrides.clear()

    def test_invalid_uuid(self):
        """
        Test the case when an invalid UUID is provided.
        """
        app.dependency_overrides[get_tags_by_video_uuid_use_case] = MagicMock()
        invalid_uuid = "invalid-uuid"

        response = client.get(f"/api/v1/videos/{invalid_uuid}/tags")
        
        assert response.status_code == 422
        assert response.json()['success'] is False
        assert response.json()['status_code'] == 1001
