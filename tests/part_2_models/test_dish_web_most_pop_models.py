import pytest
from playwright.sync_api import Page, APIRequestContext
from tests.Models.dishanyweb import DishPage
from tests.Models.dishanyapi import DishAPI, api_request_context


def test_most_pop_list(page: Page, api_request_context: APIRequestContext) -> None:
    # Given the DishAnyWhere home page is displayed

    dish_home = DishPage(page)
    dish_home.navigate()

    # Then Dish web page has its title
    dish_home.check_dish_title()

    # Then Dish web page url has ../home
    dish_home.check_dish_url_home()

    # get Dish API Most Pop list
    api_most_pop_list = DishAPI().get_api_most_pop(api_request_context, False)

    # Then Web page Carousel 'Most Popular' has correct title
    dish_home.check_most_carousel_title()

    # Get Carousel 'Popular' list
    web_most_list = dish_home.get_web_most_list()

    # And Carousel 'Popular' displays count items
    dish_home.check_item_list_count("mod most", web_most_list, len(api_most_pop_list))

    # Then Web 'Most Popular' list matches API 'Most Popular'
    dish_home.check_carousel_list("mod most", web_most_list, api_most_pop_list, False)
    # assert False

    pass
