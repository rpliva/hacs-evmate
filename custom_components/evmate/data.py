"""Custom types for evmate."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry

if TYPE_CHECKING:
    from homeassistant.loader import Integration

    from custom_components.evmate.evmate import EVMate

    from .api import IntegrationEvmateApiClient
    from .coordinator import EVMateDataUpdateCoordinator

type IntegrationEVMateConfigEntry = ConfigEntry[IntegrationEVMateData]


@dataclass
class IntegrationEVMateData:
    """Data for the EVMate integration."""

    client: IntegrationEvmateApiClient
    coordinator: EVMateDataUpdateCoordinator
    integration: Integration
    device: EVMate


class BaseSensorEntityDescription(SensorEntityDescription, frozen_or_thawed=True):
    """Base class for EVMate sensors."""

    factor: float | None = None
