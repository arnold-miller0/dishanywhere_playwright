from playwright.sync_api import Page, expect, Locator
from tests.Models.carsousel_promos import CarouselItem, PromosItem


class DishPage:
    def __init__(self, page: Page):
        self._base_url = "https://www.dishanywhere.com/"

        self._page = page
        self._version = page.locator("#footer-copyright-text")
        self._search = page.locator("#search-icon")
        self._close = page.locator("#close-icon")
        self._most_carousel = self._page.locator("#carousel-item").nth(0)
        self._avail_carousel = self._page.locator("#carousel-item").nth(1)
        self._promos_list = self._avail_carousel.locator(".carousel").nth(1)

        # carousel and promos display list max items
        self._list_display_max = 14

        # DISH Home URL Title
        self._dish_url_title = "DISH Anywhere"

    def set_browser_size(self, width:int, height: int):
        self._page.set_viewport_size({"width": width, "height": height})

    def navigate(self):
        self._page.goto(self._base_url)

    def check_title(self,
                    title: str):
        expect(self._page).to_have_title(title)

    def get_base_url(self):
        return self._base_url

    def get_url(self):
        return self._page.url

    def search_text(self,
                    text: str):
        self._search.click()
        self._page.fill("#search-input", text)

    def find_id_text(self,
                     id_attr: str,
                     text: str):
        find = self._page.locator("#" + id_attr)
        expect(find).to_have_text(text)

    def close_search(self):
        self._close.click()

    def get_web_most_carousel(self):
        return self._most_carousel

    def get_web_most_list(self):
        return self._most_carousel.locator("#card-container")

    def get_web_avail_carousel(self) -> Locator:
        return self._avail_carousel

    def get_web_avail_list(self) -> Locator:
        return self.get_web_avail_carousel().locator("div").nth(0).locator("#card-container")

    def get_web_promos_list(self) -> Locator:
        return self._promos_list.locator("#banner-card")

    def check_copyright_version(self,
                                year: int,
                                version: str):
        rights = "DISH Network L.L.C. All rights reserved. Version"
        expect(self._version).to_have_text(f"©{year} {rights} {version}")

    def check_dish_title(self):
        self.check_title(self._dish_url_title)

    def check_dish_url_home(self):
        # either on Dish Anywhere home page
        # or wait to load Dish Anywhere home page
        home_url = self.get_base_url() + "home"
        if self.get_url().endswith("/home"):
            assert self.get_url() == home_url
        else:
            self._page.wait_for_url(home_url)

    def _check_carousel_title(self,
                              carousel: Locator,
                              title: str):
        title_carousel = carousel.locator("#carousel-title")
        expect(title_carousel).to_have_text(title)

    def check_avail_carousel_title(self):
        self._check_carousel_title(self.get_web_avail_carousel(), 'Available Now')

    def check_most_carousel_title(self):
        self._check_carousel_title(self.get_web_most_carousel(), 'Most Popular')

    def check_item_list_count(self,
                              name: str,
                              item_list: Locator,
                              count: int,
                              debug=False):
        if debug:
            print(f" {name} check list item count={item_list.count()} vs count={count};")

        # must have some items
        assert item_list.count() > 0
        # list has only displayed items
        if count >= self._list_display_max:
            assert item_list.count() == self._list_display_max
        else:
            assert item_list.count() == count

    def check_carousel_list(self,
                            name: str,
                            carousel_list: Locator,
                            api_list: list[CarouselItem],
                            debug=False):
        for i in range(carousel_list.count()):
            item_carousel = carousel_list.nth(i)
            item_a_info = item_carousel.locator("a").nth(0)

            item_title = item_a_info.get_attribute("title")
            item_id = item_a_info.get_attribute("id")
            item_href = item_a_info.get_attribute("href")
            item_img_src = item_carousel.locator("img").get_attribute("src")

            if debug:
                print(f" Web {name}[{i}] title={item_title}; id={item_id}; img={item_img_src}")

            item_api = api_list[i]
            # <a title="..." > matches API "Most Popular" item's "name"
            assert item_title == item_api.get_name()

            # <a id="..." > matches API "Most Popular" item's "slug"
            assert item_id == item_api.get_slug()

            # <a href="..." > matches /franchise/ + attribute("id")
            assert "/franchise/" + item_id == item_href

            # <img src="..."> matches API "Most Popular" item's "images" "wide_poster_url"
            assert item_img_src == item_api.get_image_url()

    def check_promo_list(self,
                         name: str,
                         promo_list: Locator,
                         api_list: list[PromosItem],
                         debug=False):
        for i in range(promo_list.count()):
            item_a_info = promo_list.nth(i)

            # promos have no title
            # item_type = "None"

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

            item_img_src = item_a_info.locator("img").get_attribute("src")

            if debug:
                print(f" Web {name}[{i}] type={item_type}; id={item_id}; img={item_img_src}")

            item_api = api_list[i]
            # <a ... <div id="..." ></a> matches API "Promos" item's "id_slug" (slug last split '/')
            assert item_id == item_api.get_id_slug()

            # web item_type matches API "Promos" item type
            assert item_type == item_api.get_item_type()

            # < a href = "..." > < / a > matches API "Promos" item's "url"
            assert item_href == item_api.get_url()

            # <a ... <img src=".."></a> matches API "Most Popular" item's "image_url"
            assert item_img_src == item_api.get_image_url()