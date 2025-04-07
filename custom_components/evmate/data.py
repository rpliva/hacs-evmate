"""Custom types for evmate."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry

if TYPE_CHECKING:
    from homeassistant.loader import Integration

    from .api import IntegrationEvmateApiClient
    from .coordinator import EVMateDataUpdateCoordinator

type IntegrationEVMateConfigEntry = ConfigEntry[IntegrationEVMateData]


@dataclass
class IntegrationEVMateData:
    """Data for the EVMate integration."""

    client: IntegrationEvmateApiClient
    coordinator: EVMateDataUpdateCoordinator
    integration: Integration
