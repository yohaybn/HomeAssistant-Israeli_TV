"""Support for  IsraeliTV."""
from __future__ import annotations
import logging
from typing import Final

import os
from .guide_classes import Guide
from homeassistant.helpers.aiohttp_client import async_get_clientsession


import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA as BASE_PLATFORM_SCHEMA,
    SensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import aiohttp
from .const import (
    DOMAIN,
    ICON,
    UPDATE_TOPIC,
)


_LOGGER: Final = logging.getLogger(__name__)


_GUIDE_URL = "https://www.bevy.be/bevyfiles/israelpremium.xml"
_GUIDE_FILE = os.path.join(os.path.dirname(__file__), "userfiles/israelpremium.xml")


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the aliexpress_package_tracker sensor platform."""

    if os.path.isfile(_GUIDE_FILE):
        with open(_GUIDE_FILE, "r") as file:
            content = file.readlines()
        content = "".join(content)
        guide = Guide(content)
    else:
        _LOGGER.debug("fetching the guide first time")
        os.makedirs(os.path.dirname(_GUIDE_FILE), exist_ok=True)
        guide = await fetch_guide(hass)

    if guide is not None and guide.is_need_to_update():
        _LOGGER.debug("updating the guide")
        guide = await fetch_guide(hass)

    entities = []
    if guide is not None:
        entities.append(ChannelSensor("channel 11", guide.get_channel("ערוץ 11")))
        entities.append(ChannelSensor("channel 12", guide.get_channel("ערוץ 12")))
        entities.append(ChannelSensor("channel 13", guide.get_channel("ערוץ 13")))
        entities.append(ChannelSensor("channel 14", guide.get_channel("ערוץ 14")))
        channels = hass.data[DOMAIN].get("channels")
        if channels is not None:
            for channel in channels:
                if channel["sensor_name"] is not None:
                    entities.append(
                        ChannelSensor(
                            channel["sensor_name"], guide.get_channel(channel["name"])
                        )
                    )
    async_add_entities(entities, True)


async def fetch_guide(hass: HomeAssistant) -> Guide:
    session = async_get_clientsession(hass)
    guide = None
    try:
        response = await session.get(_GUIDE_URL)
        response.raise_for_status()
        data = await response.text()
        if data is not None:
            if "channel" in data:
                with open(_GUIDE_FILE, "w") as file:
                    file.write(data)
                    file.close()
                guide = Guide(data)
            else:
                _LOGGER.error(data)
        else:
            _LOGGER.error("Unable to retrieve guide from %s", _GUIDE_URL)

    except aiohttp.ClientError as error:
        _LOGGER.error("Error while retrieving guide: %s", error)
    return guide


class ChannelSensor(SensorEntity):
    """Representation of a ChannelSensor ."""

    _attr_icon: str = ICON

    def __init__(self, name, data) -> None:
        """Initialize the sensor."""
        _LOGGER.debug("ChannelSensor __init__ start")
        self._data = data
        self._attributes: data.get_programmes()
        self._state: data.get_current_programme().title
        self._attr_name = f"israeli_tv_{name}"

    @property
    def unique_id(self) -> str | None:
        return self._data.id

    @property
    def state(self):
        """Return the state of the device."""
        self._state = self._data.get_current_programme().title
        if self._state is None:
            return "Unavilable"
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        ret = self._data.get_programmes_per_day()
        ret["desc"] = self._data.get_current_programme().desc
        return ret

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        self.async_on_remove(
            async_dispatcher_connect(self.hass, UPDATE_TOPIC, self._force_update)
        )

    async def _force_update(self) -> None:
        """Force update of data."""
        # await self.async_update(no_throttle=True)
        self.async_write_ha_state()
