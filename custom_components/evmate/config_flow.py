"""Adds config flow for EVMate component."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS, CONF_PORT
from homeassistant.helpers import selector
from slugify import slugify

from .api import (
    IntegrationEvmateApiClient,
    IntegrationEvmateApiClientAuthenticationError,
    IntegrationEvmateApiClientCommunicationError,
    IntegrationEvmateApiClientError,
)
from .const import DOMAIN, LOGGER


class EVMateFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for EVMate."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None and len(user_input[CONF_IP_ADDRESS]) == 0:
            _errors["base"] = "missing"
        elif user_input is not None:
            try:
                await self._test_user_input(
                    address=user_input[CONF_IP_ADDRESS],
                    port=user_input[CONF_PORT],
                )
            except IntegrationEvmateApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except IntegrationEvmateApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except IntegrationEvmateApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    ## Do NOT use this in production code
                    ## The unique_id should never be something that can change
                    ## https://developers.home-assistant.io/docs/config_entries_config_flow_handler#unique-ids
                    unique_id=slugify(user_input[CONF_IP_ADDRESS])
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_IP_ADDRESS],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IP_ADDRESS, default=""): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(CONF_PORT, default=8000): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1,
                            max=65535,
                            step=1,
                            mode=selector.NumberSelectorMode.BOX,
                        )
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_user_input(self, address: str, port: int) -> None:
        """Validate user's input."""
        client = IntegrationEvmateApiClient(
            address=address,
            port=port,
            hass=self.hass,
        )
        await client.async_get_data()
