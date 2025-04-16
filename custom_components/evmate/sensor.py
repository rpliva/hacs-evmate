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
    serial_number = entry.runtime_data.coordinator.data.get("ID", None)
    if serial_number is None:
        LOGGER.error("Serial number of EVMate device is not available.")
        return

    device = EVMateDevice(
        DOMAIN + "_" + serial_number, coordinator=entry.runtime_data.coordinator
    )
    async_add_entities([device])

    async_add_entities(
        EVMateSensor(
            unique_id=device.unique_id + "_" + format_name(entity_description.name),
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
            device=device,
        )
        for entity_description in SENSOR_TYPES
    )

    async_add_entities(
        EVMateBinarySensor(
            unique_id=device.unique_id + "_" + format_name(entity_description.name),
            coordinator=entry.runtime_data.coordinator,
            description=entity_description,
            device=device,
        )
        for entity_description in BINARY_SENSOR_TYPES
    )


def get_unique_id(device: EVMateDevice, name: str) -> str:
    """Prepare the unique ID."""
    return device.unique_id + "_" + format_name(name)


def format_name(name: str) -> str:
    """Reformat the name to the unique ID."""
    return name.replace(" ", "_").replace(":", "").lower()


class EVMateDevice(SensorEntity):
    """EVMate device class."""

    def __init__(
        self,
        unique_id: str,
        coordinator: EVMateDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__()
        self.entity_description = SensorEntityDescription(
            key="ID",
            name="Serial number",
        )
        self._coordinator = coordinator
        self.serial_number = self._coordinator.data.get(
            self.entity_description.key, None
        )
        self._attr_name = self.entity_description.name
        self._attr_unique_id = unique_id
        self.entity_id = generate_entity_id(
            entity_id_format="device.{}",
            name=unique_id + "_serial_number",
            hass=coordinator.hass,
        )
        self.device_prefix = unique_id + "_"

        LOGGER.warning(
            "Added device " + self._attr_unique_id + " (" + self.entity_id + ")"
        )

    @property
    def device_info(self) -> any:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            # If desired, the name for the device could be different to the entity
            "name": self.name,
            "sw_version": self._coordinator.data.get("txt,ACTUAL SW VERSION", None),
            "model": "IoTMeter",
            "manufacturer": "EVMate",
            "serial_number": self.serial_number,
        }

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


class EVMateSensor(SensorEntity):
    """evmate Sensor class."""

    def __init__(
        self,
        unique_id: str,
        entity_description: SensorEntityDescription,
        coordinator: EVMateDataUpdateCoordinator,
        device: EVMateDevice,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__()
        self.entity_description = entity_description
        self.device = device
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
        return {"identifiers": {(DOMAIN, self.device._attr_unique_id)}}  # noqa: SLF001

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
        description: BinarySensorEntityDescription,
        coordinator: EVMateDataUpdateCoordinator,
        device: EVMateDevice,
    ) -> None:
        """Initialize the Binary sensor class."""
        super().__init__()
        self.entity_description = description
        self.device = device
        self._coordinator = coordinator
        self._attr_name = description.name
        self._attr_unique_id = unique_id
        self.entity_id = generate_entity_id(
            entity_id_format="binary_sensor.{}", name=unique_id, hass=coordinator.hass
        )

        LOGGER.warning(
            "Added binary sensor "
            + self._attr_unique_id
            + " ("
            + self.entity_id
            + ")"
        )

    @property
    def device_info(self):  # noqa: ANN201
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self.device._attr_unique_id)}}  # noqa: SLF001

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
