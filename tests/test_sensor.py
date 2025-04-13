"""Tests for sensor."""

import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.sensor import SensorEntityDescription

from custom_components.evmate.const import SENSOR_TYPES
from custom_components.evmate.coordinator import EVMateDataUpdateCoordinator
from custom_components.evmate.sensor import (
    EVMateBinarySensor,
    EVMateDevice,
    EVMateSensor,
    get_unique_id,
)


def test_get_unique_id_for_binary_sensor() -> None:
    """Test valid generation of unique ID."""
    mock_device = AsyncMock(spec=EVMateDevice)
    mock_device.unique_id = "evmate_12345"

    entity = BinarySensorEntityDescription(key="U1", name="Voltage L1")

    unique_id = get_unique_id(mock_device, entity)

    assert unique_id == "evmate_12345_voltage_l1"


def test_get_unique_id_for_sensor() -> None:
    """Test valid generation of unique ID."""
    mock_device = AsyncMock(spec=EVMateDevice)
    mock_device.unique_id = "evmate_12345"

    entity = SensorEntityDescription(key="U1", name="Voltage L1")

    unique_id = get_unique_id(mock_device, entity)

    assert unique_id == "evmate_12345_voltage_l1"


@pytest.mark.asyncio
async def test_voltage_l1_sensor() -> None:
    """Test the sensor for Voltage L1 with data from the update_setting.json fixture."""
    await _check_sensor_value("U1", 235)


@pytest.mark.asyncio
async def test_voltage_l2_sensor() -> None:
    """Test the sensor for Voltage L2 with data from the update_setting.json fixture."""
    await _check_sensor_value("U2", 233)


@pytest.mark.asyncio
async def test_automatic_update_sensor() -> None:
    """Test the automatic update with data from the update_setting.json fixture."""
    await _check_binary_sensor_value("Automatic update", "sw,AUTOMATIC UPDATE", "on")


@pytest.mark.asyncio
async def test_enable_charging_sensor() -> None:
    """Test the enable charging with data from the update_setting.json fixture."""
    await _check_binary_sensor_value("Enable charging", "sw,ENABLE CHARGING", "off")


async def _check_sensor_value(key: str, expected_state: str) -> None:
    fixtures_path = Path(__file__).parent / "fixtures"
    with Path.open(fixtures_path / "update_data.json") as file:
        update_data = json.load(file)

    # Mocks
    mock_coordinator = AsyncMock(spec=EVMateDataUpdateCoordinator)
    mock_coordinator.data = update_data
    mock_device = AsyncMock(spec=EVMateDevice)
    mock_device._attr_unique_id = "evmate_12345"  # noqa: SLF001

    # Find the right EntityDescription
    description = next(t for t in SENSOR_TYPES if t.key == key)

    # Initialize the sensor
    sensor = EVMateSensor("test", description, mock_coordinator, mock_device)

    # Call async_update to fetch data
    await sensor.async_update()

    # Assert the state and attributes for the first delivery in the fixture
    assert sensor.state == expected_state


async def _check_binary_sensor_value(name: str, key: str, expected_state: str) -> None:
    fixtures_path = Path(__file__).parent / "fixtures"
    with Path.open(fixtures_path / "update_setting.json") as file:
        update_setting = json.load(file)

    # Mocks
    mock_coordinator = AsyncMock(spec=EVMateDataUpdateCoordinator)
    mock_coordinator.data = update_setting
    mock_description = AsyncMock(spec=BinarySensorEntityDescription)
    mock_description.name = name
    mock_description.key = key
    mock_device = AsyncMock(spec=EVMateDevice)
    mock_device._attr_unique_id = "evmate_12345"  # noqa: SLF001

    # Initialize the RecentShipment sensor
    sensor = EVMateBinarySensor("test", mock_description, mock_coordinator, mock_device)

    # Call async_update to fetch data
    await sensor.async_update()

    # Assert the state and attributes for the first delivery in the fixture
    assert sensor.state == expected_state
