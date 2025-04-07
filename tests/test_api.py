"""Tests for API."""

import json
from pathlib import Path

import pytest

from custom_components.evmate.api import IntegrationEvmateApiClient


@pytest.mark.asyncio
async def test_get_data(hass, aioclient_mock) -> None:  # noqa: ANN001
    """Test case for updating data."""
    fixtures_path = Path(__file__).parent / "fixtures"
    with Path.open(fixtures_path / "update_setting.json") as file:
        update_setting = json.load(file)
    with Path.open(fixtures_path / "update_data.json") as file:
        update_data = json.load(file)
    with Path.open(fixtures_path / "update_evse.json") as file:
        update_evse = json.load(file)

    aioclient_mock.get(
        "http://192.168.0.15:8000/updateSetting",
        json=update_setting,
        status=200,
    )
    aioclient_mock.get(
        "http://192.168.0.15:8000/updateData",
        json=update_data,
        status=200,
    )
    aioclient_mock.get(
        "http://192.168.0.15:8000/updateEvse",
        json=update_evse,
        status=200,
    )

    api = IntegrationEvmateApiClient("192.168.0.15", 8000, hass)
    result = await api.async_get_data()

    assert result["DHCP"] == "1"
    assert result["EV_STATE"] == [2]
    assert result["E2tN"] == 10252  # noqa: PLR2004
