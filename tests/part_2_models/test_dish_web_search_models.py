
from playwright.sync_api import Page
from tests.Models.dishanyweb import DishPage


def test_title_url_search_version(page: Page) -> None:
    # Given the DishAnyWhere home page is displayed

    dish_home = DishPage(page)

    dish_home.navigate()

    # Then Dish web page has its title
    dish_home.check_dish_title()

    # Then Dish web page url has ../home
    dish_home.check_dish_url_home()

    # Given Search 'cBs'
    dish_home.search_text('cBs')

    # Then find "CBS sports network"
    id_attr = 'cbs_sports_network_1220-search-link'
    text = "CBS Sports Network"
    dish_home.find_id_text(id_attr, text)

    # Then close the search
    dish_home.close_search()

    # Then Dish home page copyright has year and version
    year = 2024
    version = "24.3.6"
    dish_home.check_copyright_version(year, version)

    pass
