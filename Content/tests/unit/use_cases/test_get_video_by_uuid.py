from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest
from app.application.use_cases.get_video_by_uuid import GetVideoByUUIDUseCase
from app.core.entities.video import Video
from app.core.ports.get_video_by_uuid import GetVideoByUUIDPort


class TestGetVideoByUUID:

    @pytest.mark.asyncio
    async def test_get_video_by_uuid_success(self):
        """Test the successful retrieval of a video by UUID."""
        test_time = datetime.now()

        GetVideoByUUIDPortMock = Mock(spec=GetVideoByUUIDPort)
        GetVideoByUUIDPortMock.get_video_by_uuid = AsyncMock(
            return_value=Video(
                video_uuid=UUID("12345678-1234-5678-1234-567812345678"),
                yt_id="abcd1234",
                title="Test Video",
                description="This is a test video.",
                created_at=test_time,
                modified_at=test_time,
                is_deleted=False
            )
        )
        
        get_video_by_uuid = GetVideoByUUIDUseCase(
            get_video_by_uuid=GetVideoByUUIDPortMock
        )
        video = await get_video_by_uuid.execute(
            video_uuid=UUID("12345678-1234-5678-1234-567812345678")
        )

        assert video is not None
        assert video.video_uuid == UUID("12345678-1234-5678-1234-567812345678")

        GetVideoByUUIDPortMock.get_video_by_uuid.assert_awaited_once_with(
            UUID("12345678-1234-5678-1234-567812345678")
        )

    @pytest.mark.asyncio
    async def test_get_video_by_uuid_not_found(self):
        """Test the retrieval of a video by UUID that does not exist."""
        GetVideoByUUIDPortMock = Mock(spec=GetVideoByUUIDPort)
        GetVideoByUUIDPortMock.get_video_by_uuid = AsyncMock(
            return_value=None
        )

        get_video_by_uuid = GetVideoByUUIDUseCase(
            get_video_by_uuid=GetVideoByUUIDPortMock
        )
        video = await get_video_by_uuid.execute(
            video_uuid=UUID("12345678-1234-5678-1234-567812345678")
        )

        assert video is None

        GetVideoByUUIDPortMock.get_video_by_uuid.assert_awaited_once_with(
            UUID("12345678-1234-5678-1234-567812345678")
        )
    
    @pytest.mark.asyncio
    async def test_get_video_by_uuid_invalid_uuid(self):
        """Test the retrieval of a video by an invalid UUID."""
        GetVideoByUUIDPortMock = Mock(spec=GetVideoByUUIDPort)
        get_video_by_uuid = GetVideoByUUIDUseCase(
            get_video_by_uuid=GetVideoByUUIDPortMock
        )

        with pytest.raises(ValueError, match="Invalid UUID format"):
            await get_video_by_uuid.execute(
                video_uuid="12345678-1234-5678-1234-567812345678"
            )
        GetVideoByUUIDPortMock.get_video_by_uuid.assert_not_awaited()
