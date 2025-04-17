"""Device representation of evmate."""

from custom_components.evmate.const import DOMAIN, LOGGER
from custom_components.evmate.coordinator import EVMateDataUpdateCoordinator


class EVMate:
    """EVMate device class."""

    def __init__(
        self, data: dict[str, any], coordinator: EVMateDataUpdateCoordinator
    ) -> None:
        """Initialize the EVMate device class."""
        self.serial_number = data["ID"]
        if not self.serial_number:
            LOGGER.error("Serial number of EVMate device is not available.")
            return

        self.device_id: str = DOMAIN + "_" + self.serial_number
        self.device_prefix: str = self.device_id + "_"
        self._coordinator = coordinator

    def device_info(self, key: str):  # noqa: ANN201
        """Return information to link this entity with the correct device."""
        if key == "ID":
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

    def get_unique_id(self, name: str) -> str:
        """Return UniqueID for the entity."""
        return self.device_prefix + self.format_name(name)

    def format_name(self, name: str) -> str:
        """Reformat the name to the unique ID."""
        return name.replace(" ", "_").replace(":", "").lower()
