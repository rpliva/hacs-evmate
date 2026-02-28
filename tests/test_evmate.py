"""Tests for sensor."""

import json
from pathlib import Path
from unittest.mock import AsyncMock

from homeassistant.core import HomeAssistant

from custom_components.evmate.coordinator import EVMateDataUpdateCoordinator
from custom_components.evmate.evmate import EVMate


def test_get_unique_id_for_sensor(hass: HomeAssistant) -> None:
    """Test valid generation of unique ID."""
    fixtures_path = Path(__file__).parent / "fixtures"
    with Path.open(fixtures_path / "update_data.json") as file:
        data = json.load(file)

    # Mocks
    mock_coordinator = AsyncMock(spec=EVMateDataUpdateCoordinator)
    mock_coordinator.data = data
    mock_coordinator.hass = hass

    device = EVMate(data, mock_coordinator)

    unique_id = device.get_unique_id("Voltage L1")

    assert unique_id == "evmate_12345_voltage_l1"
