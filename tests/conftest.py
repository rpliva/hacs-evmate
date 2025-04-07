"""Fixtures for testing."""

import pytest


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations) -> None:  # noqa: ANN001, ARG001
# def auto_enable_custom_integrations(enable_custom_integrations) -> None:
    """Enable custom integrations."""
    return
