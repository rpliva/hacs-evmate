"""Sensor platform for evmate."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.helpers.entity import generate_entity_id

from .const import LOGGER, SENSOR_TYPES

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

    from custom_components.evmate.evmate import EVMate

    from .coordinator import EVMateDataUpdateCoordinator
    from .data import IntegrationEVMateConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: IntegrationEVMateConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        EVMateSensor(
            device=entry.runtime_data.device,
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in SENSOR_TYPES
    )


class EVMateSensor(SensorEntity):
    """evmate Sensor class."""

    def __init__(
        self,
        device: EVMate,
        entity_description: SensorEntityDescription,
        coordinator: EVMateDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__()
        unique_id = device.get_unique_id(entity_description.name)
        self.device = device
        self.entity_description = entity_description
        self._coordinator = coordinator
        self._attr_name = entity_description.name
        self._attr_unique_id = unique_id
        self.entity_id = generate_entity_id(
            entity_id_format="sensor.{}", name=unique_id, hass=coordinator.hass
        )

        LOGGER.warning(
            "Added sensor " + self._attr_unique_id + " (" + self.entity_id + ")"
        )

    @property
    def device_info(self):  # noqa: ANN201
        """Return information to link this entity with the correct device."""
        return self.device.device_info(self.entity_description.key)

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
        if self.entity_description.factor:
            return (
                self._coordinator.data.get(self.entity_description.key, None)
                * self.entity_description.factor
            )

        return self._coordinator.data.get(self.entity_description.key, None)
