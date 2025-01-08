import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext
# import fixure 'api_request_context'
from tests.Models.dishanyapi import DishAPI, api_request_context

def test_get_api_most_pop(api_request_context: APIRequestContext) -> None:
    most_items = DishAPI().get_api_most_pop(api_request_context)
    assert len(most_items) == 15
    assert True


def test_get_api_avail_now(api_request_context: APIRequestContext) -> None:
    avail_items = DishAPI().get_api_avail_now(api_request_context)
    assert len(avail_items) == 7
    assert True


def test_get_api_promos(api_request_context: APIRequestContext) -> None:
    promos_items = DishAPI().get_api_promos_items(api_request_context)
    assert len(promos_items) == 2
    assert True
