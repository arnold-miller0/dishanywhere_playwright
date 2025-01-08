
from playwright.sync_api import Page
from tests.Models.dishanyweb import DishPage

def given_dish_home(dish_home: DishPage) -> None:
    dish_home.navigate()

    # Then Dish web page has its title
    dish_home.check_dish_title()
    # Then Dish web page url has ../home
    dish_home.check_dish_url_home()
        