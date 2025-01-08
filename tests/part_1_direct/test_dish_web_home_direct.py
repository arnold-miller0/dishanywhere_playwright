import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext
from playwright.sync_api import expect, Page
from datetime import datetime

dish_base_url = 'https://www.dishanywhere.com/'

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:

    request_context = playwright.request.new_context(
        base_url=dish_base_url
    )
    yield request_context
    request_context.dispose()


def check_carousel_list(name, carousel_list, debug=False):
    for i in range(carousel_list.count()):
        item_carousel = carousel_list.nth(i)
        item_a_info = item_carousel.locator("a").nth(0)

        # <a title="..." > matches API "Most Popular" item's "name"
        item_title = item_a_info.get_attribute("title")

        # <a id="..." > matches API "Most Popular" item's "slug"
        item_id = item_a_info.get_attribute("id")

        # <a href="..." > matches /franchise/ + attribute("id")
        item_href = item_a_info.get_attribute("href")
        assert "/franchise/" + item_id == item_href

        # <img src="..."> matches API "Most Popular" item's "images" "wide_poster_url"
        item_img_src = item_carousel.locator("img").get_attribute("src")

        if debug:
            print(f" {name}[{i}] title={item_title}; id={item_id}; img={item_img_src}")


def check_promo_list(name, promo_list, debug=False):
    for i in range(promo_list.count()):
        item_a_info = promo_list.nth(i)

        # promos have no title
        # item_type = "None"

        # <a ... <div id="..." ></a> matches API "Promos" item's "slug"
        item_id = item_a_info.locator("div").get_attribute("id")

        # when API "Promos" item's is network
        # then <a href="..."></a> matches .../networks/ + attribute("id")
        # else <a href="..."></a> matches .../franchise/ + attribute("id")
        item_href = item_a_info.get_attribute("href")
        if "/networks/" in item_href:
            item_type = "networks"
        else:
            item_type = "franchise"
        assert item_href.endswith("dishanywhere.com/" + item_type + "/" + item_id)

        # <a ... <img src=".."></a> matches API "Most Popular" item's "images"
        item_img_src = item_a_info.locator("img").get_attribute("src")

        if debug:
            print(f" {name}[{i}] type={item_type}; id={item_id}; img={item_img_src}")


def given_dish_home(page: Page) -> None:
    page.set_viewport_size({"width": 1280, "height": 960})
    page.goto(dish_base_url)
    # Then web page title is 'DISH Anywhere'
    expect(page).to_have_title("DISH Anywhere")
    # might have to wait to redirect url to home page
    # un-comment assert line to demo not yet on home page
    # assert page.url == dish_base_url + "home"

    # browser chromium normally redirects before assert
    # browser firefox and webkit normally redirect after, so need to wait
    page.wait_for_url(dish_base_url + "home")


def test_title_url_search(
        page: Page
    ) -> None:
    # Given the DishAnyWhere home page is displayed
    given_dish_home(page)

    # When Search 'cbs'
    search = page.locator("img#search-icon")
    search.click()
    page.fill("input#search-input", 'cbs')

    # Then find "CBS sports network"
    id_attr = 'cbs_sports_network_1220-search-link'
    text = "CBS Sports Network"
    results = page.locator('div#search-results-container')
    find = results.locator("a#" + id_attr)
    expect(find).to_have_text(text)

    # Then close the search
    close = page.locator("svg#close-icon")
    close.click()
    pass


def test_copyright(
        page: Page, 
        api_request_context: APIRequestContext
    ) -> None: 
    # Given the DishAnyWhere home page is displayed
    given_dish_home(page)

    # Then web page copryright, version is via current year, API config's branch
    year = str(datetime.now().year)
    
    config_url = "health/config_check"
    response = api_request_context.get(config_url, params=None, headers=None)
    assert response.ok
    config_env = response.json().get('env')
    config_branch = response.json().get('git').get('branch')
    print(f"Dish Config env: {config_env}; branch: {config_branch}")
    assert config_env == "production"
    
    version = config_branch.replace("-",".")
    copy_version = page.locator("span#footer-copyright-text")
    
    rights = " DISH Network L.L.C. All rights reserved. Version "
    expect(copy_version).to_have_text("©" + year + rights + version)
    pass


def test_Most_Pop_title_count(
        page: Page
    ) -> None: 

    # Given the DishAnyWhere home page is displayed
    given_dish_home(page)

    # Then Web page Carousel 'Most Popular' exists with at least 1 element
    most_carousel = page.locator("div#carousel-item").nth(0)
    title_carousel = most_carousel.locator("span#carousel-title")
    expect(title_carousel).to_have_text('Most Popular')
    most_list = most_carousel.locator("div#card-container")
    assert most_list.count() > 0
    check_carousel_list("most", most_list, False)
    # assert most_list.count() <= 0, "fake Failure - really passed"
    pass


def test_Avail_Now_title_count(
        page: Page
    ) -> None: 

    # Given the DishAnyWhere home page is displayed
    given_dish_home(page)

    # Then Web page Carousel 'Available Now' exists with at least 1 element
    avail_promos_carousel = page.locator("div#carousel-item").nth(1)
    title_carousel = avail_promos_carousel.locator("span#carousel-title")
    expect(title_carousel).to_have_text('Available Now')
    avail_list = avail_promos_carousel.locator("div").nth(0).locator("div#card-container")
    assert avail_list.count() > 0
    check_carousel_list("aval", avail_list, False)
    # assert avail_list.count() <= 0, "fake Failure - really passed"
    pass


def test_Promos_only_count(
        page: Page
    ) -> None: 

    # Given the DishAnyWhere home page is displayed
    given_dish_home(page)

    # Then Web page Carousel 'Promos' exists with at least 1 element
    avail_promos_carousel = page.locator('div#carousel-item').nth(1);
    promo_carousel = avail_promos_carousel.locator('div.carousel').nth(1);
    promo_list = promo_carousel.locator("a#banner-card")
    promo_list.nth(0).hover()
    # promo_list.count() has at least one element
    assert promo_list.count() > 0
    check_promo_list("promo", promo_list, True)
    # assert promo_list.count() <= 0, "fake Failure - really passed"
    pass
