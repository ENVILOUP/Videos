

from unittest.mock import AsyncMock

import pytest
from app.application.use_cases.check_external_system_health import CheckExternalSystemHealthUseCase


class TestCheckExternalSystemHealthUseCase:

    @pytest.mark.asyncio
    async def test_check_external_system_health(self):
        mock_external_system_health_check_port = AsyncMock()
        mock_external_system_health_check_port.check_health.return_value = True

        use_case = CheckExternalSystemHealthUseCase(
            external_system_heath_check_port=mock_external_system_health_check_port
        )

        result = await use_case.execute()

        assert result is True

    @pytest.mark.asyncio
    async def test_check_external_system_health_failure(self):
        mock_external_system_health_check_port = AsyncMock()
        mock_external_system_health_check_port.check_health.return_value = False

        use_case = CheckExternalSystemHealthUseCase(
            external_system_heath_check_port=mock_external_system_health_check_port
        )

        result = await use_case.execute()

        assert result is False
