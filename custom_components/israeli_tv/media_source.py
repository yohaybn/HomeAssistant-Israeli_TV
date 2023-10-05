"""Expose IsraeliTV as a media source."""
from __future__ import annotations

# import mimetypes


from homeassistant.components.media_player import BrowseError, MediaClass, MediaType
from homeassistant.components.media_source.error import Unresolvable
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_media_source(hass: HomeAssistant) -> IsraeliTVMediaSource:
    """Set up IsraeliTV Browser media source."""
    entry = hass.config_entries.async_entries(DOMAIN)
    return IsraeliTVMediaSource(hass, entry)


class IsraeliTVMediaSource(MediaSource):
    """Provide Radio stations as media sources."""

    name = "Israeli TV  Browser"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize RadioMediaSource."""
        super().__init__(DOMAIN)
        self.hass = hass
        self.entry = entry

    @property
    def stations(self) -> BrowseMediaSource | None:
        """Return the stations."""
        return self.hass.data.get(DOMAIN).get("stations")

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve selected TV station to a streaming URL."""
        stations = self.stations
        if stations is None:
            raise Unresolvable("Israeli TV Browser not initialized")

        return PlayMedia(stations.get(item.identifier).url, item.media_content_type)

    async def async_browse_media(
        self,
        item: MediaSourceItem,
    ) -> BrowseMediaSource:
        """Return media."""

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=None,
            media_class=MediaClass.CHANNEL,
            media_content_type=MediaType.VIDEO,
            title="טלוויזיה ישראלית",
            can_play=False,
            can_expand=True,
            thumbnail="https://d12rnk2x6j7ek9.cloudfront.net/wp-content/uploads/2019/09/tvilMOBILE.jpg",
            children_media_class=MediaClass.DIRECTORY,
            children=[*await self._async_build_channels()],
        )

    async def _async_build_channels(self) -> list[BrowseMediaSource]:
        items: list[BrowseMediaSource] = []

        for station in self.stations:
            if self.stations[station].url is not None:
                items.append(
                    BrowseMediaSource(
                        domain=DOMAIN,
                        identifier=station,
                        media_class=MediaClass.MUSIC,
                        media_content_type="application/vnd.apple.mpegurl",
                        title=self.stations[station].name,
                        can_play=True,
                        can_expand=False,
                        thumbnail=self.stations[station].thumbnail,
                    )
                )

        return items
