"""Test class for config flow."""

import homeassistant

from custom_components.evmate import config_flow


async def test_flow_user_step_no_input(hass: homeassistant) -> None:
    """Test appropriate error when no input is provided."""
    _result = await hass.config_entries.flow.async_init(
        config_flow.DOMAIN, context={"source": "user"}
    )
    result = await hass.config_entries.flow.async_configure(
        _result["flow_id"], user_input={}
    )
    assert result["errors"] == {"base": "missing"}
