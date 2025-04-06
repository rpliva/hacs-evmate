import pytest
import json

from unittest.mock import AsyncMock
from pathlib import Path

from custom_components.evmate.coordinator import EVMateDataUpdateCoordinator
from custom_components.evmate.binary_sensor import EVMateBinarySensor
from homeassistant.components.binary_sensor import BinarySensorEntityDescription


@pytest.mark.asyncio
async def test_automatic_update_sensor():
    """Test the Binary sensor for automatic update with data from the update_setting.json fixture."""
    await _check_binary_sensor_value("Automatic update", "sw,AUTOMATIC UPDATE", "on")

@pytest.mark.asyncio
async def test_enable_charging_sensor():
    """Test the Binary sensor for enable charging with data from the update_setting.json fixture."""
    await _check_binary_sensor_value("Enable charging", "sw,ENABLE CHARGING", "off")


async def _check_binary_sensor_value(name: str, key: str, expected_state: str):
    fixtures_path = Path(__file__).parent / "fixtures"
    with open(fixtures_path / "update_setting.json") as file:
        update_setting = json.load(file)

    # Mock the coordinator
    mock_coordinator = AsyncMock(spec=EVMateDataUpdateCoordinator)
    mock_coordinator.data = update_setting
    mock_description = AsyncMock(spec=BinarySensorEntityDescription)
    mock_description.name = name
    mock_description.key = key

    # Initialize the RecentShipment sensor
    sensor = EVMateBinarySensor("test", mock_description, mock_coordinator)

    # Call async_update to fetch data
    await sensor.async_update()

    # Assert the state and attributes for the first delivery in the fixture
    assert sensor.state == expected_state
    # assert sensor.extra_state_attributes == {
    #     "full_description": "Wireless Mouse Set",
    #     "tracking_number": "8217400125612976",
    #     "date_expected": "tomorrow",
    #     "event_date": "yesterday",
    #     "event_location": "Harrisburg, PA, USA",
    #     "status": "Delivery in transit.",
    #     "carrier": "Fedex",
    # }
