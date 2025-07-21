import logging
import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .tuya_api import fetch_device_localkeys

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    _LOGGER.info("✅ getlocalkey component initialized. Configure via config flow.")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    _LOGGER.info("🔐 Setting up getlocalkey with config entry.")
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await fetch_device_localkeys(entry.data, _LOGGER)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    _LOGGER.info("🧹 Unloading getlocalkey config entry.")
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
