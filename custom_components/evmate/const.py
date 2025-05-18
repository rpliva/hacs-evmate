"""Constants for evmate."""

from logging import Logger, getLogger

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.sensor.const import SensorDeviceClass

from custom_components.evmate.data import BaseSensorEntityDescription

LOGGER: Logger = getLogger(__package__)

DOMAIN = "evmate"

EVSE_ID = "evse_id"
CURRENT = "current"

SENSOR_TYPES: tuple[BaseSensorEntityDescription, ...] = (
    BaseSensorEntityDescription(
        key="ID",
        name="Serial number",
    ),
    BaseSensorEntityDescription(
        key="U1",
        name="Voltage L1",
        native_unit_of_measurement="V",
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    BaseSensorEntityDescription(
        key="U2",
        name="Voltage L2",
        native_unit_of_measurement="V",
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    BaseSensorEntityDescription(
        key="U3",
        name="Voltage L3",
        native_unit_of_measurement="V",
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    BaseSensorEntityDescription(
        key="I1",
        name="Current L1",
        native_unit_of_measurement="mA",
        device_class=SensorDeviceClass.CURRENT,
        factor=10,
    ),
    BaseSensorEntityDescription(
        key="I2",
        name="Current L2",
        native_unit_of_measurement="mA",
        device_class=SensorDeviceClass.CURRENT,
        factor=10,
    ),
    BaseSensorEntityDescription(
        key="I3",
        name="Current L3",
        native_unit_of_measurement="mA",
        device_class=SensorDeviceClass.CURRENT,
        factor=10,
    ),
    BaseSensorEntityDescription(
        key="P1",
        name="Power L1",
        native_unit_of_measurement="W",
        device_class=SensorDeviceClass.POWER,
    ),
    BaseSensorEntityDescription(
        key="P2",
        name="Power L2",
        native_unit_of_measurement="W",
        device_class=SensorDeviceClass.POWER,
    ),
    BaseSensorEntityDescription(
        key="P3",
        name="Power L3",
        native_unit_of_measurement="W",
        device_class=SensorDeviceClass.POWER,
    ),
    BaseSensorEntityDescription(
        key="F1",
        name="Power factor L1",
        device_class=SensorDeviceClass.POWER_FACTOR,
        factor=0.01,
    ),
    BaseSensorEntityDescription(
        key="F2",
        name="Power factor L2",
        device_class=SensorDeviceClass.POWER_FACTOR,
        factor=0.01,
    ),
    BaseSensorEntityDescription(
        key="F3",
        name="Power factor L3",
        device_class=SensorDeviceClass.POWER_FACTOR,
        factor=0.01,
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
    BinarySensorEntityDescription(
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
    ),
    BinarySensorEntityDescription(
        key="RELAY",
        name="RELAY",
    ),
)
