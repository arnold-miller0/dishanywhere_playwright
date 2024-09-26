
from playwright.sync_api import expect, Page


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


def test_title_url_search_more(page: Page) -> None:
    # Given the DishAnyWhere home page is displayed
    dish_base_url = 'https://www.dishanywhere.com/'
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

    # When Search 'cbs'
    search = page.locator("#search-icon")
    search.click()
    page.fill("#search-input", 'cbs')

    # Then find "CBS sports network"
    id_attr = 'cbs_sports_network_1220-search-link'
    text = "CBS Sports Network"
    find = page.locator("#" + id_attr)
    expect(find).to_have_text(text)

    # Then close the search
    close = page.locator("#close-icon")
    close.click()

    # Then web page version is "24.3.6"
    copy_version = page.locator("#footer-copyright-text")
    year = "2024"
    rights = " DISH Network L.L.C. All rights reserved. Version "
    version_text = "24.3.6"
    expect(copy_version).to_have_text("©" + year + rights + version_text)

    # Then Web page Carousel 'Most Popular' matches API 'Most Popular'
    most_carousel = page.locator("#carousel-item").nth(0)
    title_carousel = most_carousel.locator("#carousel-title")
    expect(title_carousel).to_have_text('Most Popular')
    most_list = most_carousel.locator("#card-container")
    # most_list.count() matches API Most Popular list count
    assert most_list.count() > 0
    check_carousel_list("most", most_list, False)
    # assert most_list.count() <= 0, "fake Failure - really passed"

    # Then Web page Carousel 'Available Now and Promos'
    #      matches API 'Available Now' and API 'Promos'
    avail_promos_carousel = page.locator("#carousel-item").nth(1)
    title_carousel = avail_promos_carousel.locator("#carousel-title")
    expect(title_carousel).to_have_text('Available Now')

    avail_list = avail_promos_carousel.locator("div").nth(0).locator("#card-container")
    # avail_list.count() matches API "Available Now" list count
    assert avail_list.count() > 0
    check_carousel_list("aval", avail_list, False)
    # assert avail_list.count() <= 0, "fake Failure - really passed"

    # promo_carousel = avail_promos_carousel.locator(".carousel").nth(1)
    promo_carousel = page.locator(".carousel").nth(2)
    promo_list = promo_carousel.locator("#banner-card")
    # promo_list.count() matches API "Promos" list
    assert promo_list.count() > 0
    check_promo_list("promo", promo_list, True)
    # assert promo_list.count() <= 0, "fake Failure - really passed"

    pass
