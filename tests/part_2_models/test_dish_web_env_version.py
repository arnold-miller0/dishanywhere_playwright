
from playwright.sync_api import Page, APIRequestContext
# import fixure 'web_request_context'
from tests.Models.dishanyweb import DishPage, web_request_context
from tests.part_2_models.help_dish_web_methods import given_dish_home
from datetime import datetime

def test_copyright_version(
        page: Page, 
        web_request_context: APIRequestContext
    ) -> None:

    # Given the DishAnyWhere home page is displayed
    dish_home = DishPage(page)
    given_dish_home(dish_home)

    # Then Dish home page copyright has year and version
    dish_home.set_config_env_version(web_request_context, True)

    web_env = dish_home.get_web_env()
    cfg_env = dish_home.get_config_env()
    assert web_env == cfg_env

    year = str(datetime.now().year)
    version = dish_home.get_config_version()
    dish_home.check_copyright_version(year, version)

    pass
