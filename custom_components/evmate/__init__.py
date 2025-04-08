"""
Custom integration to integrate evmate with Home Assistant.

For more details about this integration, please refer to
https://github.com/rpliva/evmate
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import CONF_IP_ADDRESS, CONF_PORT, Platform
from homeassistant.loader import async_get_loaded_integration

from .api import IntegrationEvmateApiClient
from .const import DOMAIN, LOGGER
from .coordinator import EVMateDataUpdateCoordinator
from .data import IntegrationEVMateData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import IntegrationEVMateConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: IntegrationEVMateConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = EVMateDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(hours=1),
    )
    entry.runtime_data = IntegrationEVMateData(
        client=IntegrationEvmateApiClient(
            address=entry.data[CONF_IP_ADDRESS],
            port=entry.data[CONF_PORT],
            hass=hass,
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: IntegrationEVMateConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: IntegrationEVMateConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
