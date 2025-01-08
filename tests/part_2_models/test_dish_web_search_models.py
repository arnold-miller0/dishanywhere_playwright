
from playwright.sync_api import Page
# import fixure 'web_request_context'
from tests.Models.dishanyweb import DishPage
from tests.part_2_models.help_dish_web_methods import given_dish_home


def test_title_url_search(
        page: Page
    ) -> None:
    # Given the DishAnyWhere home page is displayed

    dish_home = DishPage(page)
    given_dish_home(dish_home)
    
    # Given Search 'cBs'
    dish_home.search_text('cBs')

    # Then find "CBS sports network"
    id_attr = 'cbs_sports_network_1220-search-link'
    text = "CBS Sports Network"
    dish_home.find_id_text(id_attr, text)

    # Then close the search
    dish_home.close_search()

    pass
