import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:

    request_context = playwright.request.new_context(
        base_url="https://radish.dishanywhere.com/"
    )

    yield request_context
    request_context.dispose()


def test_get_carousel_group(api_request_context: APIRequestContext) -> None:
    url = "v20/dol/carousel_group/home.json"
    params = {"totalItems": 15}
    headers = {"Accept": "application/vnd.echostar.franchise+json;version=1"}
    response = api_request_context.get(url, params=params, headers=headers)
    assert response.ok

    groups = response.json()
    assert len(groups) > 0
    for i in range(len(groups)):
        group = groups[i]
        items = group.get('items')
        print(f" group[{i}] title={group.get('title')}; items={len(items)}")
        assert len(items) > 0
        for j in range(len(items)):
            item = items[j]
            print(f" \t web dir item[{j}] kind={item.get('kind')}; locked={item.get('is_locked')}; name={item.get('name')}; slug={item.get('slug')}")

    # assert len(groups) < 0


def test_get_promos(api_request_context: APIRequestContext) -> None:
    url = "v20/dol/home/promos.json"
    params = None
    headers = {"Accept": "application/vnd.echostar.franchise+json;version=1"}
    response = api_request_context.get(url, params=params, headers=headers)
    assert response.ok

    promos = response.json()
    assert len(promos) > 0
    for promo in promos:
        print(f" web dir promo: slug={promo.get('slug')}; url={promo.get('url')}")
    # assert len(promos) < 0


def test_get_list_most_watched(api_request_context: APIRequestContext) -> None:
    url = "list"
    params = {"list_name": "most_watched_channels",
              "totalItems": 10,
              "offset": 0}
    headers = {"Accept": "application/vnd.echostar.franchises+json;version=1"}
    response = api_request_context.get(url, params=params, headers=headers)
    assert response.status == 200

    most = response.json()
    print(f" most watched: {most}")
    assert most["name"] == "Most Watched Channels"
    assert most["count"] == 0
    assert len(most["franchises"]) == 0


def test_get_ad_free_content(api_request_context: APIRequestContext) -> None:
    url = "/v20/dol/networks/home.json"
    params = {"ad_free_content_only": "true"}
    headers = {"Accept": "*/*"}
    response = api_request_context.get(url, params=params, headers=headers)
    assert response.ok

    ad_free = response.json()
    assert len(ad_free) == 0


def test_get_sample_show_info(api_request_context: APIRequestContext) -> None:
    url = "/franchise/big_brother_e3726073"
    params = None
    headers = {"Accept": "application/vnd.echostar.franchise+json;version=6"}
    response = api_request_context.get(url, params=params, headers=headers)
    assert response.ok


