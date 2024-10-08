"""The IsraeliTV integration."""
import logging
from types import SimpleNamespace

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from radios import FilterBy, Order, RadioBrowser, Station
import json
import aiohttp
from .const import DOMAIN
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)

import voluptuous as vol

_LOGGER = logging.getLogger(__name__)


GET_URL_SCHEMA = vol.Schema({vol.Required("channel_name"): str})


async def async_setup(hass, config):
    """Handle the service call."""
    _LOGGER.debug("async_setup")
    hass.data[DOMAIN] = config[DOMAIN]

    async def get_channel_12_url() -> str:
        """Handle the service call."""
        _LOGGER.debug("get_channel_12_url")
        try:
            session = async_get_clientsession(hass)
            headers = {
                'Content-Length': '0',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',
                'Accept': 'application/json'
            }
            
            async with session.post(
                "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp?et=gt&lp=/hls/live/512033/CH2LIVE_HIGH/index.m3u8&rv=AKAMAI",
                headers=headers
            ) as response:
                src = await response.text()
                _LOGGER.debug("async_setup json: %s", json.loads(src)["tickets"])
                url = f'https://mako-streaming.akamaized.net/stream/hls/live/2033791/k12dvr/index.m3u8?{json.loads(src)["tickets"][0]["ticket"]}'
                return url
        except aiohttp.ClientError as error:
            _LOGGER.error("Error while retrieving channel 12 URL: %s", error)

    def play_cahnnel(media_player, url):
        """play_cahnnel"""
        service_data = {
            "entity_id": media_player,
            "media_content_id": url,
            "media_content_type": "channel",
        }
        _LOGGER.debug(service_data)
        hass.services.call("media_player", "play_media", service_data)

    def play_custom_channel(call):
        """Handle the service call."""
        _LOGGER.debug("play_custom_channel")
        media_player_entity_id = call.data.get("entity_id")
        url = call.data.get("url")
        if url is None:
            name = call.data.get("channel_name")
            channel = next(
                (
                    channel
                    for channel in config[DOMAIN]["channels"]
                    if channel["sensor_name"] == name
                ),
                None,
            )
            if channel is not None:
                url = channel["url"]
            play_cahnnel(media_player_entity_id, url)

    def play_channel_11(call):
        """Handle the service call."""
        _LOGGER.debug("play_channel_11")
        media_player_entity_id = call.data.get("entity_id")
        url = "https://kan11.media.kan.org.il/hls/live/2024514/2024514/master.m3u8"
        play_cahnnel(media_player_entity_id, url)

    async def play_channel_12(call):
        """Handle the service call."""
        _LOGGER.debug("play_channel_12")
        media_player_entity_id = call.data.get("entity_id")

        service_data = {
            "entity_id": media_player_entity_id,
            "media_content_id": await get_channel_12_url,
            "media_content_type": "video",
        }
        _LOGGER.debug(service_data)
        hass.async_create_task(
            hass.services.async_call("media_player", "play_media", service_data)
        )

    def play_channel_13(call):
        """Handle the service call."""
        _LOGGER.debug("play_channel_13")
        media_player_entity_id = call.data.get("entity_id")
        url = "https://d18b0e6mopany4.cloudfront.net/out/v1/08bc71cf0a0f4712b6b03c732b0e6d25/index.m3u8"
        play_cahnnel(media_player_entity_id, url)

    def play_channel_14(call):
        """Handle the service call."""
        _LOGGER.debug("play_channel_14")
        media_player_entity_id = call.data.get("entity_id")
        url = "https://now14.g-mana.live/media/91517161-44ab-4e46-af70-e9fe26117d2e/mainManifest.m3u8"
        play_cahnnel(media_player_entity_id, url)

    async def sync_stations():
        hass.data[DOMAIN]["stations"] = {}
        hass.data[DOMAIN]["stations"]["channel_11"] = SimpleNamespace(
            url="https://kan11.media.kan.org.il/hls/live/2024514/2024514/master.m3u8",
            thumbnail="https://yt3.googleusercontent.com/ytc/APkrFKa3XnZWBtBhxfhUOLSKy2bPZFZP6SDuLJTMHl4VuA=s900-c-k-c0x00ffffff-no-rj",
            name="כאן",
        )

        hass.data[DOMAIN]["stations"]["channel_12"] = SimpleNamespace(
            url=await get_channel_12_url(),
            thumbnail="https://upload.wikimedia.org/wikipedia/he/thumb/f/f0/Keshet12_2018.svg/1200px-Keshet12_2018.svg.png",
            name="ערוץ 12",
        )
        hass.data[DOMAIN]["stations"]["channel_13"] = SimpleNamespace(
            url="https://d18b0e6mopany4.cloudfront.net/out/v1/08bc71cf0a0f4712b6b03c732b0e6d25/index.m3u8",
            thumbnail="https://upload.wikimedia.org/wikipedia/he/thumb/1/17/Reshet13Logo2022.svg/1200px-Reshet13Logo2022.svg.png",
            name="ערוץ 13",
        )
        hass.data[DOMAIN]["stations"]["channel_14"] = SimpleNamespace(
            url="https://now14.g-mana.live/media/91517161-44ab-4e46-af70-e9fe26117d2e/mainManifest.m3u8",
            thumbnail="https://yt3.googleusercontent.com/_zuu3BebkXpOJWlNB2d2NRXlpQF1VgqDB3ocmn8dqbWKyOoPIHWyNpitbgu8Ra5ssQTw_FdMX_4=s900-c-k-c0x00ffffff-no-rj",
            name="ערוץ 14",
        )
        channels = hass.data[DOMAIN].get("channels")
        if channels is not None:
            for channel in channels:
                hass.data[DOMAIN]["stations"][
                    channel.get("sensor_name")
                ] = SimpleNamespace(
                    url=channel.get("url"),
                    thumbnail=channel.get("thumbnail"),
                    name=channel.get("name"),
                )

    async def get_channel_url(call) -> ServiceResponse:
        """Handle the service call."""
        _LOGGER.debug("get_channel_url")
        await sync_stations()
        channel_no = call.data.get("channel_name")
        return {"url": hass.data[DOMAIN]["stations"].get(channel_no).url}

    # return hass.data[DOMAIN].get(channel_no)

    await sync_stations()
    use_defaults = config[DOMAIN].get("use_defaults")
    if use_defaults is None or use_defaults:
        hass.services.async_register(DOMAIN, "play_channel_11", play_channel_11)
        hass.services.async_register(DOMAIN, "play_channel_12", play_channel_12)
        hass.services.async_register(DOMAIN, "play_channel_13", play_channel_13)
        hass.services.async_register(DOMAIN, "play_channel_14", play_channel_14)

    hass.services.async_register(DOMAIN, "play_custom_channel", play_custom_channel)
    hass.services.async_register(
        DOMAIN,
        "get_channel_url",
        get_channel_url,
        schema=GET_URL_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )
    # Return boolean to indicate that initialization was successful.
    return True
