import pytest
from playwright.sync_api import Page, APIRequestContext
from tests.Models.dishanyweb import DishPage
from tests.Models.dishanyapi import DishAPI, api_request_context


def test_avail_now_list(page: Page, api_request_context: APIRequestContext) -> None:
    # Given the DishAnyWhere home page is displayed

    dish_home = DishPage(page)
    dish_home.navigate()

    # Then Dish web page has its title
    dish_home.check_dish_title()

    # Then Dish web page url has ../home
    dish_home.check_dish_url_home()

    # get Dish API Most Pop list
    api_avail_now_list = DishAPI().get_api_avail_now(api_request_context, False)

    # Then Web page Carousel 'Available Now' has correct title
    dish_home.check_avail_carousel_title()

    # And Carousel 'Available Now' has displayed item count
    web_avail_list = dish_home.get_web_avail_list()
    # And Carousel 'Available Now' displays count items
    dish_home.check_item_list_count("mod aval", web_avail_list, len(api_avail_now_list))

    # And Carousel 'Available Now' matches API 'Available Now'
    dish_home.check_carousel_list("mod aval", web_avail_list, api_avail_now_list, False)
    # assert False

    pass
