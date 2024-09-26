
import pytest
from playwright.sync_api import Page, APIRequestContext
from tests.Models.dishanyweb import DishPage
from tests.Models.dishanyapi import DishAPI, api_request_context


@pytest.fixture(scope="function")
def dish_api(api_request_context: APIRequestContext):
    return DishAPI()


def navigate_to_dish_home_search(page: Page):
    DishPage(page).navigate()
    DishPage(page).check_dish_title()
    DishPage(page).check_dish_url_home()