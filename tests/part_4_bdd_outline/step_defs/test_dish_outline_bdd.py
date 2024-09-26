import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, APIRequestContext
from tests.Models.dishanyweb import DishPage
from tests.Models.dishanyapi import DishAPI, api_request_context
from tests.part_3_bdd_normal.step_defs.common_steps import navigate_to_dish_home_search, dish_api

scenarios('../features/dish_home_outline.feature')

@given(parsers.parse('On DishAnyWhere Home size "{width:d}" x "{height:d}"'))
def navigate_to_dish_home_size(page: Page, width:int, height:int):
    DishPage(page).set_browser_size(width, height)
    navigate_to_dish_home_search(page)

def navigate_to_dish_home_page(page: Page):
    navigate_to_dish_home_search(page)
    # assert False, "Fake failure, really PASS!"

@given('On DishAnyWhere Home page')
def navigate_to_dish_home_page(page: Page):
    navigate_to_dish_home_search(page)
    # assert False, "Fake failure, really PASS!"

@when(parsers.parse('Search for "{item}"'))
def search_for_item(page: Page, item:str):
    DishPage(page).search_text(item)

@then(parsers.parse('Finds id "{id_attr}" with "{text}"'))
def finds_id_attr_with_text(page: Page, id_attr, text):
    print(f"Finds id={id_attr}; text={text};")
    DishPage(page).find_id_text(id_attr, text)

@then('Close Search')
def close_search(page: Page):
    DishPage(page).close_search()

@then(parsers.parse('Displays copyright "{year:d}" and version "{deployed}"'))
def display_copyright_version(page: Page, year:int, deployed: str):
    print(f"copyright year={year}; version={deployed};")
    DishPage(page).check_copyright_version(year, deployed)

@when(parsers.parse('Get Dish API "{name}" List'))
def get_dish_api_list(name:str,
                      dish_api: DishAPI,
                      api_request_context: APIRequestContext):
    list_type  = name.lower()[0]
    if list_type == 'a':
        api_list = dish_api.get_api_avail_now(api_request_context, False)
    elif list_type == 'm':
        api_list = dish_api.get_api_most_pop(api_request_context, False)
    elif list_type == 'p':
        api_list = dish_api.get_api_promos_items(api_request_context, False)
    else:
        assert False, not_valid_list_name(name)
    assert len(api_list) > 0


@then(parsers.parse('Dish Home "{name}" List has Title'))
def check_dish_home_list_title(page: Page, name:str):
    list_type  = name.lower()[0]
    if list_type == 'a':
        DishPage(page).check_avail_carousel_title()
    elif list_type == 'm':
        DishPage(page).check_most_carousel_title()
    elif list_type == 'p':
        # Promotion list has same tile as Most Popular Title
        DishPage(page).check_most_carousel_title()
        assert True
    else:
        assert False, not_valid_list_name(name)


@then(parsers.parse('Dish Home "{name}" List Matches API'))
def check_dish_home_list_match_api(page: Page, name:str,
                                   dish_api: DishAPI,
                                   api_request_context: APIRequestContext):
    list_type  = name.lower()[0]
    if list_type == 'a':
        home_list = DishPage(page).get_web_avail_list()
        api_list = dish_api.avail_items
    elif list_type == 'm':
        home_list = DishPage(page).get_web_most_list()
        api_list = dish_api.most_items
    elif list_type == 'p':
        home_list = DishPage(page).get_web_promos_list()
        api_list = dish_api.promo_items
    else:
        assert False, not_valid_list_name(name)
    DishPage(page).check_item_list_count("out " + name, home_list, len(api_list))
    if list_type == 'p':
        # Promos List has different API check than Avail and Most Lists
        DishPage(page).check_promo_list("out " + name, home_list, api_list, True)
    else:
        DishPage(page).check_carousel_list("out " + name, home_list, api_list, True)


def not_valid_list_name(name:str) -> str:
    return f"not valid list name '{name}'; expected: 'Avail', 'Most', 'Pop'"