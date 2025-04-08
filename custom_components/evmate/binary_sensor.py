"""Binary sensor platform for evmate."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .const import BINARY_SENSOR_TYPES

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EVMateDataUpdateCoordinator
    from .data import IntegrationEVMateConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: IntegrationEVMateConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        EVMateBinarySensor(
            # unique_id=(
            #     entry.unique_id
            #     + "-"
            #     + entity_description.key.replace(",", "_").replace(" ", "_")
            # ),
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in BINARY_SENSOR_TYPES
    )


class EVMateBinarySensor(BinarySensorEntity):
    """EVMate Binary sensor class."""

    def __init__(
        self,
        # unique_id: str,
        description: BinarySensorEntityDescription,
        coordinator: EVMateDataUpdateCoordinator,
    ) -> None:
        """Initialize the Binary sensor class."""
        super().__init__()
        self.entity_description = description
        self._coordinator = coordinator
        self._attr_name = description.name
        # self._attr_unique_id = unique_id  # noqa: ERA001

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
    def is_on(self) -> bool:
        """Return the state of the binary sensor."""
        return self._coordinator.data.get(self.entity_description.key, "0") == "1"
