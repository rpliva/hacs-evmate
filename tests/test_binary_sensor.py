"""Tests for Binary sensors."""

import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from homeassistant.components.binary_sensor import BinarySensorEntityDescription

from custom_components.evmate.binary_sensor import EVMateBinarySensor
from custom_components.evmate.coordinator import EVMateDataUpdateCoordinator


@pytest.mark.asyncio
async def test_automatic_update_sensor() -> None:
    """Test the automatic update with data from the update_setting.json fixture."""
    await _check_binary_sensor_value("Automatic update", "sw,AUTOMATIC UPDATE", "on")


@pytest.mark.asyncio
async def test_enable_charging_sensor() -> None:
    """Test the enable charging with data from the update_setting.json fixture."""
    await _check_binary_sensor_value("Enable charging", "sw,ENABLE CHARGING", "off")


async def _check_binary_sensor_value(name: str, key: str, expected_state: str) -> None:
    fixtures_path = Path(__file__).parent / "fixtures"
    with Path.open(fixtures_path / "update_setting.json") as file:
        update_setting = json.load(file)

    # Mock the coordinator
    mock_coordinator = AsyncMock(spec=EVMateDataUpdateCoordinator)
    mock_coordinator.data = update_setting
    mock_description = AsyncMock(spec=BinarySensorEntityDescription)
    mock_description.name = name
    mock_description.key = key

    # Initialize the RecentShipment sensor
    sensor = EVMateBinarySensor(mock_description, mock_coordinator)

    # Call async_update to fetch data
    await sensor.async_update()

    # Assert the state and attributes for the first delivery in the fixture
    assert sensor.state == expected_state
