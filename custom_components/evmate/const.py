"""Constants for evmate."""

from logging import Logger, getLogger

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.sensor.const import SensorDeviceClass

LOGGER: Logger = getLogger(__package__)

DOMAIN = "evmate"


SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="U1",
        name="Voltage L1",
        native_unit_of_measurement="V",
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    SensorEntityDescription(
        key="U2",
        name="Vlatage L2",
        native_unit_of_measurement="V",
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    SensorEntityDescription(
        key="U3",
        name="Voltage L3",
        native_unit_of_measurement="V",
        device_class=SensorDeviceClass.VOLTAGE,
    ),
)

BINARY_SENSOR_TYPES: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="sw,AUTOMATIC UPDATE",
        name="Automatic update",
    ),
    BinarySensorEntityDescription(
        key="sw,ENABLE CHARGING",
        name="Enable charging",
    ),
)
