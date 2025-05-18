"""Exposed services."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from custom_components.evmate.const import CURRENT, DOMAIN, EVSE_ID

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant, ServiceCall

    from custom_components.evmate.api import IntegrationEvmateApiClient


_LOGGER = logging.getLogger(__name__)

SET_CURRENT_SCHEMA = vol.Schema(
    {
        vol.Required(EVSE_ID): cv.positive_int,
        vol.Required(CURRENT): cv.positive_int,
    }
)


async def async_register_services(
    hass: HomeAssistant, api: IntegrationEvmateApiClient
) -> None:
    """Register ParcelApp services."""
    client = api

    async def async_set_current(call: ServiceCall) -> None:
        """Set current value for the specific EVSE device."""
        _LOGGER.info("SET_CURRENT service - Received data", call.data)  # noqa: PLE1205
        evse_id = call.data[EVSE_ID]
        current = call.data[CURRENT]
        request = (
            '{"variable":"inp,EVSE' + str(evse_id) + '","value":"' + str(current) + '"}'
        )
        _LOGGER.info("SET_CURRENT service - requsting change - ", request)  # noqa: PLE1205
        client.async_post_setting(str.encode(request))

    hass.services.async_register(
        DOMAIN,
        "set_current",
        async_set_current,
        schema=SET_CURRENT_SCHEMA,
    )
