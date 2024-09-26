
class CarouselItem:

    def __init__(self, is_api: bool, kind: str, name: str,
                 slug: str, is_locked: bool, image_url: str):
        self._is_api = is_api
        self._kind = kind
        self._name = name
        self._slug = slug
        self._is_locked = is_locked
        self._image_url = image_url

    def get_is_api(self) -> bool:
        return self._is_api

    def get_kind(self) -> str:
        return self._kind

    def get_name(self) -> str:
        return self._name

    def get_slug(self) -> str:
        return self._slug

    def get_is_locked(self) -> bool:
        return self._is_locked

    def get_image_url(self) -> str:
        return self._image_url


class PromosItem:

    def __init__(self, is_api: bool, item_type: str,
                 slug: str, id_slug: str, url: str, image_url: str):
        self._is_api = is_api
        self._item_type = item_type
        self._full_slug = slug
        self._id_slug = id_slug
        self._url = url
        self._image_url = image_url

    def get_is_api(self) -> bool:
        return self._is_api

    def get_item_type(self) -> str:
        return self._item_type

    def get_full_slug(self) -> str:
        return self._full_slug

    def get_id_slug(self) -> str:
        return self._id_slug

    def get_url(self) -> str:
        return self._url

    def get_image_url(self) -> str:
        return self._image_url
