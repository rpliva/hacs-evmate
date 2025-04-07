"""Sample API Client."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.aiohttp_client import async_get_clientsession

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


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
        """Sample API Client."""
        self._hass = hass
        self._session = async_get_clientsession(self._hass)
        self._host = "http://" + address + ":" + str(port) + "/"

    async def async_get_data(self) -> dict[str, Any]:
        """Get data from the API."""
        result = {}
        result.update(await self._endpoint_request("updateSetting"))
        result.update(await self._endpoint_request("updateData"))
        result.update(await self._endpoint_request("updateEvse"))
        return result

    async def _endpoint_request(self, endpoint: str) -> dict[str, Any]:
        try:
            response = await self._session.get(self._host + endpoint)
            response.raise_for_status()
            payload = await response.text()
            raw_json = json.loads(payload)
        except Exception as e:  # noqa: BLE001
            raw_json = {"error": e}

        return raw_json
