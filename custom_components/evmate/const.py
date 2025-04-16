"""Constants for evmate."""

from logging import Logger, getLogger

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.sensor.const import SensorDeviceClass

LOGGER: Logger = getLogger(__package__)

DOMAIN = "evmate"


SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="ID",
        name="Serial number",
    ),
    SensorEntityDescription(
        key="U1",
        name="Voltage L1",
        native_unit_of_measurement="V",
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    SensorEntityDescription(
        key="U2",
        name="Voltage L2",
        native_unit_of_measurement="V",
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    SensorEntityDescription(
        key="U3",
        name="Voltage L3",
        native_unit_of_measurement="V",
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    """    SensorEntityDescription(
        key="A3",
        name="Current L1",
        native_unit_of_measurement="A",
        device_class=SensorDeviceClass.CURRENT,
    ),
    SensorEntityDescription(
        key="A2",
        name="Current L2",
        native_unit_of_measurement="A",
        device_class=SensorDeviceClass.CURRENT,
    ),
    SensorEntityDescription(
        key="A3",
        name="Current L3",
        native_unit_of_measurement="A",
        device_class=SensorDeviceClass.CURRENT,
    ),
    SensorEntityDescription(
        key="P1",
        name="Power L1",
        native_unit_of_measurement="kW",
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="P2",
        name="Power L2",
        native_unit_of_measurement="kW",
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="P3",
        name="Power L3",
        native_unit_of_measurement="kW",
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="R1",
        name="Power factor L1",
        device_class=SensorDeviceClass.POWER_FACTOR,
    ),
    SensorEntityDescription(
        key="R2",
        name="Power factor L2",
        device_class=SensorDeviceClass.POWER_FACTOR,
    ),
    SensorEntityDescription(
        key="R3",
        name="Power factor L3",
        device_class=SensorDeviceClass.POWER_FACTOR,
    ),""",
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
    """    BinarySensorEntityDescription(
        key="sw,ENABLE BALANCING",
        name="Enable balancing",
    ),
    BinarySensorEntityDescription(
        key="sw,WHEN AC IN: RELAY ON",
        name="When AC IN: relay ON",
    ),
    BinarySensorEntityDescription(
        key="sw,WHEN OVERFLOW: RELAY ON",
        name="When overflow: relay ON",
    ),
    BinarySensorEntityDescription(
        key="sw,WHEN AC IN: CHARGING",
        name="When AC IN: charging",
    ),
    BinarySensorEntityDescription(
        key="sw,AC IN ACTIVE: HIGH",
        name="AC IN active: high",
    ),
    BinarySensorEntityDescription(
        key="sw,TESTING SOFTWARE",
        name="Testing software",
    ),
    BinarySensorEntityDescription(
        key="sw,Wi-Fi AP",
        name="WiFi AP",
    ),
    BinarySensorEntityDescription(
        key="sw,MODBUS-TCP",
        name="MODBUS TCP",
    ),
    BinarySensorEntityDescription(
        key="sw,P-E15-GUARD",
        name="P-E15 GUARD",
    ),""",
)
