"""Channel 12 (Mako) stream URL lookup. No Home Assistant imports."""
from __future__ import annotations

import json
import logging

import aiohttp

_LOGGER = logging.getLogger(__name__)

TICKET_URL = (
    "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp"
    "?et=gt&lp=/hls/live/512033/CH2LIVE_HIGH/index.m3u8&rv=AKAMAI"
)
STREAM_URL = "https://mako-streaming.akamaized.net/stream/hls/live/2033791/k12dvr/index.m3u8"
HEADERS = {
    "Content-Length": "0",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    "Accept": "application/json",
}


def parse_ticket_response(text: str) -> str | None:
    """Return the stream URL from the ticket response, or None if it is not a valid ticket.

    The server can answer with a non-JSON page (for example a Radware block
    page), which must not raise.
    """
    try:
        ticket = json.loads(text)["tickets"][0]["ticket"]
    except (ValueError, KeyError, IndexError, TypeError):
        _LOGGER.warning(
            "Channel 12 ticket response is not valid (starts with: %r)", text[:100]
        )
        return None
    return f"{STREAM_URL}?{ticket}"


async def async_get_channel_12_url(session) -> str | None:
    """Fetch a Channel 12 stream URL. Returns None on any failure."""
    try:
        async with session.post(TICKET_URL, headers=HEADERS) as response:
            text = await response.text()
    except (aiohttp.ClientError, TimeoutError) as error:
        _LOGGER.error("Error while retrieving channel 12 URL: %s", error)
        return None
    return parse_ticket_response(text)
