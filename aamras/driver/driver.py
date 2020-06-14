"""Driver wrapper."""

from typing import Optional
import urllib.parse

from selenium.common.exceptions import InvalidCookieDomainException
from selenium.webdriver.remote.webdriver import WebDriver

from ..util import LoggerMixin
from .cookies import CookieManagerMixin
from .element import ElementTraverserMixin

class Driver(LoggerMixin, CookieManagerMixin, ElementTraverserMixin):
    """Abstraction/wrapper of selenium WebDriver."""
    driver: WebDriver

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.close()

    @property
    def title(self):
        """Title of the current page."""
        return self.driver.title

    @property
    def url(self):
        """Current URL."""
        return self.driver.current_url

    @property
    def dom_root(self):
        return self.driver

    def close(self):
        """Save cookies and shut down driver."""
        self.log.info("driver shutdown initiated")
        self._save_cookies()

        self.log.info("cleaning up dependencies")
        self.driver.quit()

    def _load_cookies(self) -> None:
        """Load stored cookies and attempt to set them in the driver"""
        self.log.info("loading cookies")
        cookies = self.cookies.get()

        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
            except InvalidCookieDomainException:
                pass

    def _save_cookies(self):
        """Save cookies, adding any new cookies from the driver"""
        cookies = self.driver.get_cookies()
        self.cookies.save(cookies)

    def get(self, url: str) -> None:
        """Navigate to a provided url.

        :param url: relative or absolute path, or full URL to navigate to
        """
        url_new = urllib.parse.urljoin(self.driver.current_url, url)

        self.log.info("navigate to %s" % (url_new))
        self.driver.get(url_new)

        self._load_cookies()
        self.log_page()

    def click(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            tag: Optional[str] = None) -> None:
        """Click an element matching provided criteria.

        See :meth:`element` for documentation on criteria.
        """
        element = self.element(id_, name, class_, tag)
        element.click()

        self.log_page()

    def submit(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            tag: Optional[str] = None) -> None:
        """Submit an element matching provided criteria.

        See :meth:`element` for documentation on criteria.
        """
        element = self.element(id_, name, class_, tag)
        element.click()

        self.log_page()

    def type(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            text: Optional[str] = None) -> None:
        """Send text input to an element matching provided criteria.

        See :meth:`element` for documentation on criteria.
        """
        element = self.element(id_, name, class_)
        element.type(text)

    def screenshot(self, file_path: str):
        """Save a screenshot of the browser window.

        :param file_path: path of file to save screenshot to
        """
        self.log.info("saving screenshot to '%s'" % (file_path))
        self.driver.get_screenshot_as_file(file_path)

    def save_source(self, file_path: str) -> None:
        """Save source code of current page.

        :param file_path: path of file to save source to
        """
        self.log.info(f"write page source to {file_path}")
        with open(file_path, "w") as file_:
            file_.write(str(self.driver.page_source))

    def log_page(self) -> None:
        """Write page information to log."""
        self.log.info(
            f"page title is {self.driver.title} ({self.driver.current_url})")
