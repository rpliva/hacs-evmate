"""Tests for sensor."""

import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.core import HomeAssistant

from custom_components.evmate.const import SENSOR_TYPES
from custom_components.evmate.coordinator import EVMateDataUpdateCoordinator
from custom_components.evmate.sensor import (
    EVMateBinarySensor,
    EVMateSensor,
    format_name,
)


def test_get_unique_id_for_sensor() -> None:
    """Test valid generation of unique ID."""
    unique_id = format_name("Voltage L1")

    assert unique_id == "voltage_l1"


@pytest.mark.asyncio
async def test_voltage_l1_sensor(hass: HomeAssistant) -> None:
    """Test the sensor for Voltage L1 with data from the update_setting.json fixture."""
    await _check_sensor_value(hass, "U1", 235)


@pytest.mark.asyncio
async def test_voltage_l2_sensor(hass: HomeAssistant) -> None:
    """Test the sensor for Voltage L2 with data from the update_setting.json fixture."""
    await _check_sensor_value(hass, "U2", 233)


@pytest.mark.asyncio
async def test_automatic_update_sensor(hass: HomeAssistant) -> None:
    """Test the automatic update with data from the update_setting.json fixture."""
    await _check_binary_sensor_value(
        hass, "Automatic update", "sw,AUTOMATIC UPDATE", "on"
    )


@pytest.mark.asyncio
async def test_enable_charging_sensor(hass: HomeAssistant) -> None:
    """Test the enable charging with data from the update_setting.json fixture."""
    await _check_binary_sensor_value(
        hass, "Enable charging", "sw,ENABLE CHARGING", "off"
    )


async def _check_sensor_value(
    hass: HomeAssistant, key: str, expected_state: str
) -> None:
    fixtures_path = Path(__file__).parent / "fixtures"
    with Path.open(fixtures_path / "update_data.json") as file:
        update_data = json.load(file)

    # Mocks
    mock_coordinator = AsyncMock(spec=EVMateDataUpdateCoordinator)
    mock_coordinator.data = update_data
    mock_coordinator.hass = hass

    # Find the right EntityDescription
    description = next(t for t in SENSOR_TYPES if t.key == key)

    # Initialize the sensor
    sensor = EVMateSensor("test", description, mock_coordinator)

    # Call async_update to fetch data
    await sensor.async_update()

    # Assert the state and attributes for the first delivery in the fixture
    assert sensor.state == expected_state


async def _check_binary_sensor_value(
    hass: HomeAssistant, name: str, key: str, expected_state: str
) -> None:
    fixtures_path = Path(__file__).parent / "fixtures"
    with Path.open(fixtures_path / "update_setting.json") as file:
        update_setting = json.load(file)

    # Mocks
    mock_coordinator = AsyncMock(spec=EVMateDataUpdateCoordinator)
    mock_coordinator.data = update_setting
    mock_coordinator.hass = hass
    mock_description = AsyncMock(spec=BinarySensorEntityDescription)
    mock_description.name = name
    mock_description.key = key

    # Initialize the RecentShipment sensor
    sensor = EVMateBinarySensor("test", mock_description, mock_coordinator)

    # Call async_update to fetch data
    await sensor.async_update()

    # Assert the state and attributes for the first delivery in the fixture
    assert sensor.state == expected_state
