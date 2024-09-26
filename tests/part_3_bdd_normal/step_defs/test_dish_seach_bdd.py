import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import Page
from tests.Models.dishanyweb import DishPage
from tests.part_3_bdd_normal.step_defs.common_steps import navigate_to_dish_home_search

scenarios('../features/dish_home_search.feature')


@given('On DishAnyWhere Home page')
def navigate_to_dish_home_page(page: Page):
    navigate_to_dish_home_search(page)
    # assert False, "Fake failure, really PASS!"


@when('Search for cbs')
def search_for_cbs(page: Page):
    DishPage(page).search_text('CBs')


@then('Finds CBS Sports Network')
def finds_cbs_sports_network(page: Page):
    id_attr = 'cbs_sports_network_1220-search-link'
    text = "CBS Sports Network"
    DishPage(page).find_id_text(id_attr, text)


@then('Close Search')
def close_search(page: Page):
    DishPage(page).close_search()


@then('Displays copyright and deployed version')
def display_copyright_version(page: Page):
    year = 2024
    version = "24.3.6"
    DishPage(page).check_copyright_version(year, version)
