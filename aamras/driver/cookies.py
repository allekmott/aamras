
from typing import cast, Dict, List, Mapping, Optional, Union
import json
import os.path

from ..util import LoggerMixin

COOKIE_FILE = "cookies.json"

def with_valid_expiry(cookie: Mapping) -> Mapping:
    """Convert cookie expiry to milliseconds, if necessary.

    :param cookie: Coookie to be converted
    """
    if "expiry" in cookie and isinstance(cookie["expiry"], float):
        cookie_updated = dict(cookie)
        cookie_updated["expiry"] = int(cookie["expiry"] * 1000)

        return cookie_updated
    else:
        return cookie

class CookieManager(LoggerMixin):
    _cookies: Optional[List[Mapping]]

    def __init__(self, file_: str = COOKIE_FILE):
        self.cookie_file = file_
        self._cookies = None

    @property
    def cookies(self) -> List[Mapping]:
        """Data structure housing cookies.

        Mapping of domain -> list of associated cookies.
        """
        if self._cookies is None:
            self.cookies = self._load()

        return cast(List[Mapping], self._cookies)

    @cookies.setter
    def cookies(self, cookies: List[Mapping]):
        self._cookies = cookies

    def get(self) -> List[Mapping]:
        """Get stored cookies."""
        return self.cookies

    def add(self, cookies: Union[Dict, List[Dict]]) -> None:
        """Merge cookies into cookie list

        :param cookies: Cookies to be merged in
        """
        if not isinstance(cookies, list):
            cookies = [cookies]

        new_domains = set(map(lambda c: c["domain"], cookies))
        def not_replaced(cookie: Mapping) -> bool:
            return cookie["domain"] not in new_domains

        new_cookie_list = list(filter(not_replaced, self.cookies))
        new_cookie_list.extend(cookies)

        self.cookies = new_cookie_list

    def _load(self) -> List[Mapping]:
        """Load cookies from cookie file"""
        self.log.info(f"reading saved cookies from {self.cookie_file}")

        if not os.path.exists(self.cookie_file):
            self.log.info(f"cookie file not found: {self.cookie_file}")
            return []

        def is_compatible_cookie(cookie):
            return is_compatible(domain, cookie["domain"])

        with open(self.cookie_file, "r") as file_:
            data = file_.read()
            cookies = json.loads(data)

        return list(map(with_valid_expiry, cookies))

    def save(self, cookies: Optional[Union[Dict, List[Dict]]] = None) -> None:
        if cookies:
            self.add(cookies)

        self.log.info((
            f"saving {len(self.cookies)} cookies "
            f"to {self.cookie_file}"))

        with open(self.cookie_file, "w") as file_:
            file_.write(json.dumps(self.cookies))

class CookieManagerMixin:
    _cookies: CookieManager

    @property
    def cookies(self) -> CookieManager:
        if not hasattr(self, "_cookies") or not self._cookies:
            self._cookies = CookieManager()

        return self._cookies
