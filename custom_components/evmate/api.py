"""Sample API Client."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


UPDATE_SETTING = "updateSetting"
UPDATE_DATA = "updateData"
UPDATE_EVSE = "updateEvse"


class IntegrationEvmateApiClientError(Exception):
    """Exception to indicate a general API error."""


class IntegrationEvmateApiClientCommunicationError(
    IntegrationEvmateApiClientError,
):
    """Exception to indicate a communication error."""


class IntegrationEvmateApiClientAuthenticationError(
    IntegrationEvmateApiClientError,
):
    """Exception to indicate an authentication error."""


class IntegrationEvmateApiClient:
    """EVMate API Client."""

    def __init__(
        self,
        address: str,
        port: int,
        hass: HomeAssistant,
    ) -> None:
        """EVMate API Client."""
        self._hass = hass
        self._session = async_get_clientsession(self._hass)
        self._host = "http://" + address + ":" + str(int(port)) + "/"

    async def async_get_data(self) -> dict[str, Any]:
        """Get data from the API."""
        result = {}
        result.update(await self._endpoint_get_request(UPDATE_SETTING))
        result.update(await self._endpoint_get_request(UPDATE_DATA))
        result.update(await self._endpoint_get_request(UPDATE_EVSE))
        return result

    async def async_post_setting(self, data: bytes) -> bool:
        """Set device setting via API."""
        try:
            response = await self._session.post(self._host + UPDATE_SETTING, data=data)
            response.raise_for_status()
            payload = await response.text()
            raw_json = json.loads(payload)
        except Exception as e:  # noqa: BLE001
            raw_json = {"error": e}
            LOGGER.error(e, stack_info=True, exc_info=True)

        return raw_json["process"]

    async def _endpoint_get_request(self, endpoint: str) -> dict[str, Any]:
        try:
            response = await self._session.get(self._host + endpoint)
            response.raise_for_status()
            payload = await response.text()
            raw_json = json.loads(payload)
        except Exception as e:  # noqa: BLE001
            raw_json = {"error": e}
            LOGGER.error(e, stack_info=True, exc_info=True)

        return raw_json
