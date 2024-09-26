import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import Page, APIRequestContext
from tests.Models.dishanyweb import DishPage
from tests.Models.dishanyapi import DishAPI, api_request_context
from tests.part_3_bdd_normal.step_defs.common_steps import navigate_to_dish_home_search, dish_api


scenarios('../features/dish_home_carousels.feature')


@given('On DishAnyWhere Home page')
def navigate_to_dish_home_page(page: Page):
    navigate_to_dish_home_search(page)


@when('Get Dish API Avail Now List')
def get_dish_api_avail_now_list(dish_api: DishAPI, api_request_context: APIRequestContext):
    dish_api.get_api_avail_now(api_request_context, False)
    assert len(dish_api.avail_items) > 0


@then('Dish Home Avail Now List has Title')
def dish_home_avail_now_matches_api(page: Page):
    DishPage(page).check_avail_carousel_title()


@then('Dish Home Avail Now List Matches API')
def dish_home_avail_now_matches_api(page: Page, dish_api: DishAPI):
    home_list = DishPage(page).get_web_avail_list()
    api_list = dish_api.avail_items
    DishPage(page).check_item_list_count("bdd aval", home_list, len(api_list))
    DishPage(page).check_carousel_list("bdd avail", home_list, api_list, True)


@when('Get Dish API Most Popular List')
def get_dish_api_most_pop_list(dish_api: DishAPI, api_request_context: APIRequestContext):
    dish_api.get_api_most_pop(api_request_context, False)
    assert len(dish_api.most_items) > 0


@then('Dish Home Most Popular List has Title')
def dish_home_avail_most_pop_api(page: Page):
    DishPage(page).check_most_carousel_title()


@then('Dish Home Most Popular List Matches API')
def dish_home_avail_most_pop_api(page: Page, dish_api: DishAPI):
    home_list = DishPage(page).get_web_most_list()
    api_list = dish_api.most_items
    DishPage(page).check_item_list_count("bdd most", home_list, len(api_list))
    DishPage(page).check_carousel_list("bdd most", home_list, api_list, True)
