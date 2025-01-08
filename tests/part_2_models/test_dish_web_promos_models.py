import pytest
from playwright.sync_api import Page, APIRequestContext
from tests.Models.dishanyweb import DishPage
# import fixure 'api_request_context'
from tests.Models.dishanyapi import DishAPI, api_request_context
from tests.part_2_models.help_dish_web_methods import given_dish_home


def test_promos_list(page: Page, api_request_context: APIRequestContext) -> None:
    # Given the DishAnyWhere home page is displayed

    dish_home = DishPage(page)
    given_dish_home(dish_home)

    # delay wait for api avail now list response just like browser api request sequence
    DishAPI().get_api_avail_now(api_request_context)
    # get Dish API Promos list
    api_promos_list = DishAPI().get_api_promos_items(api_request_context)

    # Then Web page Carousel 'Promos' matches API 'Promos'
    web_promos_list = dish_home.get_web_promos_list()

    dish_home.check_item_list_count("mod promo", web_promos_list, len(api_promos_list))

    # And there is at least 1 'Promos'
    assert web_promos_list.count() > 0
    # promos_list.count() matches API "Promos" list count
    assert web_promos_list.count() == len(api_promos_list)
    dish_home.check_promo_list("mod promo", web_promos_list, api_promos_list, False)
    # assert False

    pass
