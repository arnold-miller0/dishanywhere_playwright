import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import Page, APIRequestContext
from tests.Models.dishanyweb import DishPage
from tests.Models.dishanyapi import DishAPI, api_request_context
from tests.part_3_bdd_normal.step_defs.common_steps import navigate_to_dish_home_search, dish_api

scenarios('../features/dish_home_promos.feature')


@given('On DishAnyWhere Home page')
def navigate_to_dish_home_page(page: Page):
    navigate_to_dish_home_search(page)

@when('Get Dish API Most and Promo Lists')
def get_dish_api_promotion_list(dish_api: DishAPI, api_request_context: APIRequestContext):
    # get API Most Popular before Promo List to be like to Web Page
    dish_api.get_api_most_pop(api_request_context, False)
    dish_api.get_api_promos_items(api_request_context, False)
    assert len(dish_api.promo_items) > 0


@then('Dish Home Promotion List Matches API')
def dish_home_avail_now_matches_api(page: Page, dish_api:DishAPI):
    api_list = dish_api.promo_items
    home_list = DishPage(page).get_web_promos_list()
    #if home_list.count() <= 0:
    #    print(f"no promo list; wait 1 second then try again")
    #    page.wait_for_timeout(1000)
    #    home_list = DishPage(page).get_web_promos_list()
    DishPage(page).check_item_list_count("bdd promo", home_list, len(api_list))
    DishPage(page).check_promo_list("bdd promo", home_list, api_list, True)

