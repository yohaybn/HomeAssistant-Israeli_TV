"""The IsraeliTV integration."""
import logging

from homeassistant.helpers.aiohttp_client import async_get_clientsession
import json
import aiohttp
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Handle the service call."""
    _LOGGER.debug("async_setup")
    hass.data[DOMAIN] = config[DOMAIN]

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
                    if channel["name"] == name
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
        try:
            session = async_get_clientsession(hass)
            async with session.post(
                "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp?et=gt&lp=/hls/live/512033/CH2LIVE_HIGH/index.m3u8&rv=AKAMAI"
            ) as response:
                src = await response.text()
                _LOGGER.debug("async_setup json: %s", json.loads(src)["tickets"])
                url = f'https://mako-streaming.akamaized.net/stream/hls/live/2033791/k12dvr/index.m3u8?{json.loads(src)["tickets"][0]["ticket"]}'
                service_data = {
                    "entity_id": media_player_entity_id,
                    "media_content_id": url,
                    "media_content_type": "video",
                }
                _LOGGER.debug(service_data)
                hass.async_create_task(
                    hass.services.async_call("media_player", "play_media", service_data)
                )
                # hass.services.call("media_player", "play_media", service_data)
        except aiohttp.ClientError as error:
            _LOGGER.error(
                "Error while retrieving package data for  track_packages: %s", error
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

    use_defaults = config[DOMAIN].get("use_defaults")
    if use_defaults is None or use_defaults:
        hass.services.async_register(DOMAIN, "play_channel_11", play_channel_11)
        hass.services.async_register(DOMAIN, "play_channel_12", play_channel_12)
        hass.services.async_register(DOMAIN, "play_channel_13", play_channel_13)
        hass.services.async_register(DOMAIN, "play_channel_14", play_channel_14)

    hass.services.async_register(DOMAIN, "play_custom_channel", play_custom_channel)
    # Return boolean to indicate that initialization was successful.
    return True
