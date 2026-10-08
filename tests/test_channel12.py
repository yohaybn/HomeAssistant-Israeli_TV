import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "custom_components" / "israeli_tv"))

from channel12 import STREAM_URL, async_get_channel_12_url, parse_ticket_response  # noqa: E402

GOOD = '{"caseId":"1","status":"Success","tickets":[{"vendor":"AKAMAI","ticket":"hdnea=abc","url":"/x"}]}'
BLOCK = '<!DOCTYPE html>\n<html><head><title>Radware Block Page</title></head></html>'


class FakeResponse:
    def __init__(self, text):
        self._t = text

    async def text(self):
        return self._t

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


class FakeSession:
    def __init__(self, text):
        self.text = text

    def post(self, *a, **k):
        return FakeResponse(self.text)


def test_valid_ticket():
    assert parse_ticket_response(GOOD) == f"{STREAM_URL}?hdnea=abc"


def test_radware_block_page_returns_none():
    assert parse_ticket_response(BLOCK) is None


def test_empty_and_malformed_return_none():
    for t in ("", "{}", '{"tickets":[]}', "[]", "null"):
        assert parse_ticket_response(t) is None


def test_async_lookup_with_block_page_does_not_raise():
    assert asyncio.run(async_get_channel_12_url(FakeSession(BLOCK))) is None
    assert asyncio.run(async_get_channel_12_url(FakeSession(GOOD))).endswith("hdnea=abc")
