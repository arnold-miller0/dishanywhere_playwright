import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext
from tests.Models.carsousel_promos import CarouselItem, PromosItem


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url=DishAPI().base_url
    )
    yield request_context
    request_context.dispose()


class DishAPI:

    def __init__(self):
        self.base_url = "https://radish.dishanywhere.com/"
        self.most_items = []
        self.avail_items = []
        self.promo_items = []

    def get_api_most_pop(self,
                         api_request_context: APIRequestContext,
                         debug=False):
        carousels = self._get_group_carousels(api_request_context)
        self.most_items = self._get_carousel_items(0, carousels, debug)
        return self.most_items

    def get_api_avail_now(self,
                          api_request_context: APIRequestContext,
                          debug=False):
        carousels = self._get_group_carousels(api_request_context)
        self.avail_items = self._get_carousel_items(1, carousels, debug)
        return self.avail_items

    def _get_group_carousels(self,
                             api_request_context: APIRequestContext):
        url = "v20/dol/carousel_group/home.json"
        params = {"totalItems": 15}
        headers = {"Accept": "application/vnd.echostar.franchise+json;version=1"}
        response = api_request_context.get(url, params=params, headers=headers)
        assert response.ok
        return response.json()

    def _get_carousel_items(self,
                            index: int,
                            carousels,
                            debug=False
                            ) -> list[CarouselItem]:
        item_list = []
        if len(carousels) <= index:
            return item_list

        group = carousels[index]
        carousel = group.get('items')
        print(f" title={group.get('title')}; items={len(carousel)}")
        for j in range(len(carousel)):
            item = carousel[j]
            if debug:
                print(
                    f" \t API item[{j}] kind={item.get('kind')}; locked={item.get('is_locked')}; "
                    f"name={item.get('name')}; slug={item.get('slug')}")

            some = CarouselItem(True,
                                item.get('kind'),
                                item.get('name'),
                                item.get('slug'),
                                item.get('is_locked'),
                                item.get('images').get('wide_poster_url'))

            item_list.append(some)
        return item_list

    def get_api_promos_items(self,
                             api_request_context: APIRequestContext,
                             debug=False
                             ) -> list[PromosItem]:
        url = "v20/dol/home/promos.json"
        params = None
        headers = {"Accept": "application/vnd.echostar.franchise+json;version=1"}
        response = api_request_context.get(url, params=params, headers=headers)
        assert response.ok

        promos = response.json()

        item_list = []
        if len(promos) <= 0:
            self.promo_items = item_list
            return item_list

        for promo in promos:
            url = promo.get('url')
            # real slug (id) is the 'url' last split via '/'
            id_slug = url.split("/")[-1]
            if "/networks/" in url:
                item_type = "networks"
            else:
                item_type = "franchise"

            if debug:
                print(f" API promo: type={item_type}; slug={promo.get('slug')}; "
                      f" id={id_slug}; url={url}")

            item = PromosItem(True, item_type, promo.get('slug'), id_slug,
                              promo.get('url'), promo.get('image_url'))

            item_list.append(item)

        self.promo_items = item_list
        return item_list
