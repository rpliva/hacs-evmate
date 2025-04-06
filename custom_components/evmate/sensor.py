"""Sensor platform for evmate."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .coordinator import EVMateDataUpdateCoordinator
from .data import IntegrationEVMateConfigEntry
from .const import SENSOR_TYPES


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: IntegrationEVMateConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        EVMateSensor(
            f"{entry.unique_id}-{entity_description.key.replace(",", "_").replace(" ", "_")}",
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in SENSOR_TYPES
    )


class EVMateSensor(SensorEntity):
    """evmate Sensor class."""

    def __init__(
        self,
        unique_id: str,
        entity_description: SensorEntityDescription,
        coordinator: EVMateDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__()
        self.entity_description = entity_description
        self._coordinator = coordinator
        self._attr_name = entity_description.name
        self._attr_unique_id = unique_id

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self) -> None:
        """Get the latest data from OWM and updates the states."""
        await self._coordinator.async_request_refresh()

    @property
    def native_value(self) -> StateType:
        """Return the state of the device."""
        return self._coordinator.data.get(self.entity_description.key, None)

    # @property
    # def extra_state_attributes(self):
    #     """Return entity specific state attributes."""
    #     return {
    #         ATTR_API_TODAY_HOURLY_PRICES: self._coordinator.data.get(
    #             ATTR_API_TODAY_HOURLY_PRICES
    #         ),
    #         ATTR_API_TOMORROW_HOURLY_PRICES: self._coordinator.data.get(
    #             ATTR_API_TOMORROW_HOURLY_PRICES
    #         ),
    #     }