import os
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Set execute permission for the script
    script_path = hass.config.path('custom_components/bvk_smartreader/getBvkSuezData.sh')
    if os.path.exists(script_path):
        os.chmod(script_path, 0o755)

    update_interval = entry.options.get(CONF_UPDATE_INTERVAL, 8)
    _LOGGER.debug(f"Setting up entry with update interval: {update_interval} hours")

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
