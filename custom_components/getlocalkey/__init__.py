import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "getlocalkey"

async def async_setup(hass, config):
    _LOGGER.info("✅ getlocalkey component initialized. Configure via config flow.")
    return True

async def async_setup_entry(hass, entry):
    _LOGGER.info("🔐 Setting up getlocalkey with config entry.")
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    return True

async def async_unload_entry(hass, entry):
    _LOGGER.info("🧹 Unloading getlocalkey config entry.")
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
