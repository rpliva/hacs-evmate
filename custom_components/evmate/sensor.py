"""Sensor platform for evmate."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.helpers.entity import generate_entity_id

from .const import BINARY_SENSOR_TYPES, DOMAIN, LOGGER, SENSOR_TYPES

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

    from .coordinator import EVMateDataUpdateCoordinator
    from .data import IntegrationEVMateConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: IntegrationEVMateConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    await entry.runtime_data.coordinator._async_update_data()  # noqa: SLF001
    serial_number: str | None = entry.runtime_data.coordinator.data.get("ID", None)
    if not serial_number:
        LOGGER.error("Serial number of EVMate device is not available.")
        return

    device_id: str = DOMAIN + "_" + serial_number
    device_prefix: str = device_id + "_"

    for entity_description in SENSOR_TYPES:
        LOGGER.warning(entity_description)

    await async_add_entities(
        EVMateSensor(
            unique_id=device_prefix + format_name(entity_description.name),
            device_id=device_id,
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in SENSOR_TYPES
    )

    await async_add_entities(
        EVMateBinarySensor(
            unique_id=device_prefix + format_name(entity_description.name),
            device_id=device_id,
            coordinator=entry.runtime_data.coordinator,
            description=entity_description,
        )
        for entity_description in BINARY_SENSOR_TYPES
    )


def format_name(name: str) -> str:
    """Reformat the name to the unique ID."""
    return name.replace(" ", "_").replace(":", "").lower()


class EVMateSensor(SensorEntity):
    """evmate Sensor class."""

    def __init__(
        self,
        unique_id: str,
        device_id: str,
        entity_description: SensorEntityDescription,
        coordinator: EVMateDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__()
        self.device_id = device_id
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
        if self.entity_description.key == "ID":
            return {
                "identifiers": {(DOMAIN, self.device_id)},
                # If desired, the name for the device could be different to the entity
                "name": "EVMate IoTMeter - " + self._coordinator.data.get("ID", None),
                "sw_version": self._coordinator.data.get("txt,ACTUAL SW VERSION", None),
                "model": "IoTMeter",
                "manufacturer": "EVMate",
                "serial_number": self._coordinator.data.get("ID", None),
            }
        return {"identifiers": {(DOMAIN, self.device_id)}}

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


class EVMateBinarySensor(BinarySensorEntity):
    """EVMate Binary sensor class."""

    def __init__(
        self,
        unique_id: str,
        device_id: str,
        description: BinarySensorEntityDescription,
        coordinator: EVMateDataUpdateCoordinator,
    ) -> None:
        """Initialize the Binary sensor class."""
        super().__init__()
        self.device_id = device_id
        self.entity_description = description
        self._coordinator = coordinator
        self._attr_name = description.name
        self._attr_unique_id = unique_id
        self.entity_id = generate_entity_id(
            entity_id_format="binary_sensor.{}", name=unique_id, hass=coordinator.hass
        )

        LOGGER.warning(
            "Added binary sensor " + self._attr_unique_id + " (" + self.entity_id + ")"
        )

    @property
    def device_info(self):  # noqa: ANN201
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self.device_id)}}

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
