import pytest
import json

from unittest.mock import AsyncMock
from pathlib import Path

from custom_components.evmate.coordinator import EVMateDataUpdateCoordinator
from custom_components.evmate.sensor import EVMateSensor
from custom_components.evmate.const import SENSOR_TYPES
from homeassistant.components.sensor import SensorEntityDescription


@pytest.mark.asyncio
async def test_voltage_l1_sensor():
    """Test the sensor for Voltage L1 with data from the update_setting.json fixture."""
    await _check_sensor_value("U1", 235)

@pytest.mark.asyncio
async def test_voltage_l2_sensor():
    """Test the sensor for Voltage L2 with data from the update_setting.json fixture."""
    await _check_sensor_value("U2", 233)


async def _check_sensor_value(key: str, expected_state: str):
    fixtures_path = Path(__file__).parent / "fixtures"
    with open(fixtures_path / "update_data.json") as file:
        update_data = json.load(file)

    # Mock the coordinator
    mock_coordinator = AsyncMock(spec=EVMateDataUpdateCoordinator)
    mock_coordinator.data = update_data

    # Find the right EntityDescription
    description = next(t for t in SENSOR_TYPES if t.key == key)

    # Initialize the sensor
    sensor = EVMateSensor("test", description, mock_coordinator)

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
