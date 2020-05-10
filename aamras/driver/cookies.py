
import json
import os.path
from typing import cast, Mapping

from ..util import LoggerMixin

COOKIE_FILE = "cookies.json"

class CookieManager(LoggerMixin):
    def __init__(self, file_: str = COOKIE_FILE):
        self.cookie_file = COOKIE_FILE

    def load(self) -> Mapping:
        self.log.info(f"reading saved cookies from {self.cookie_file}")

        if not os.path.exists(self.cookie_file):
            self.log.info(f"cookie file not found: {self.cookie_file}")
            return {}

        with open(self.cookie_file, "r") as file_:
            data = file_.read()
            cookies = json.loads(data)

            for cookie in cookies:
                if "expiry" in cookie and isinstance(cookie["expiry"], float):
                    cookie["expiry"] = int(cookie["expiry"] * 1000)

        self.log.info(f"found {len(cookies)} saved cookies")
        return cast(Mapping, cookies)

    def save(self, cookies: Mapping) -> None:
        self.log.info(f"saving {len(cookies)} cookies to {self.cookie_file}")

        with open(self.cookie_file, "w") as file_:
            file_.write(json.dumps(cookies))

class CookieManagerMixin:
    _cookies: CookieManager

    @property
    def cookies(self) -> CookieManager:
        if not hasattr(self, "_cookies") or not self._cookies:
            self._cookies = CookieManager()

        return self._cookies
