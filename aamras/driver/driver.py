
from typing import Callable, List, Optional
import urllib.parse

from selenium.common.exceptions import InvalidCookieDomainException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ..util import LoggerMixin
from .cookies import CookieManagerMixin

def _attr_filter(attr: str, value: str) -> Callable[[WebElement], bool]:
    def filter_(element: WebElement) -> bool:
        return bool(element.get_attribute(attr) == value)

    return filter_

def _tag_filter(tag: str) -> Callable[[WebElement], bool]:
    def filter_(element: WebElement) -> bool:
        return bool(element.tag_name == tag)

    return filter_

def _class_filter(class_: str) -> Callable[[WebElement], bool]:
    def filter_(element: WebElement) -> bool:
        classes = element.get_attribute("class").split(" ")
        return class_ in classes

    return filter_

class Driver(LoggerMixin, CookieManagerMixin):
    driver: WebDriver

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.close()

    @property
    def title(self):
        return self.driver.title

    @property
    def url(self):
        return self.driver.current_url

    def close(self):
        self.log.info("driver shutdown initiated")
        self._save_cookies()

        self.log.info("cleaning up dependencies")
        self.driver.quit()

    def _load_cookies(self) -> None:
        self.log.info("loading cookies")
        cookies = self.cookies.get()

        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
            except InvalidCookieDomainException:
                pass

    def _save_cookies(self):
        cookies = self.driver.get_cookies()
        self.cookies.save(cookies)

    def get(self, url: str) -> None:
        url_new = urllib.parse.urljoin(self.driver.current_url, url)

        self.log.info("navigate to %s" % (url_new))
        self.driver.get(url_new)

        self._load_cookies()
        self.log_page()

    def elements(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            tag: Optional[str] = None) -> List[WebElement]:
        identifiers_defined = list(filter(bool, [id_, name, class_, tag]))
        assert identifiers_defined, \
            "At least one of id_, name, class_, or tag must be defined"

        filters: List[Callable[[WebElement], bool]] = []
        matches: List[WebElement] = []

        if id_:
            matches.extend(self.driver.find_elements_by_id(id_))
            filters.append(_attr_filter("id", id_))

        if name:
            matches.extend(self.driver.find_elements_by_name(name))
            filters.append(_attr_filter("name", name))

        if class_:
            matches.extend(self.driver.find_elements_by_class_name(class_))
            filters.append(_class_filter(class_))

        if tag:
            matches.extend(self.driver.find_elements_by_tag_name(tag))
            filters.append(_tag_filter(tag))

        matches_filtered = matches
        for filter_ in filters:
            matches_filtered = list(filter(filter_, matches))

        return matches_filtered

    def element(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            tag: Optional[str] = None) -> WebElement:
        identifiers_defined = list(filter(bool, [id_, name, class_, tag]))
        assert len(identifiers_defined) == 1, \
            "Either id_, name, class_, or tag must be defined"

        if id_:
            return self.driver.find_element_by_id(id_)
        elif name:
            return self.driver.find_element_by_name(name)
        elif class_:
            return self.driver.find_element_by_class_name(class_)
        elif tag:
            return self.driver.find_element_by_tag_name(tag)

    def _log_element_action(
            self,
            action: str,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            tag: Optional[str] = None):
        params = {
            "id": id_,
            "name": name,
            "class": class_,
            "tag": tag
        }

        criteria_string = ", ".join(
            [f"{k}=\"{v}\"" for (k, v) in params.items() if v])
        self.log.info(f"{action} element ({criteria_string})")

    def click(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            tag: Optional[str] = None) -> None:
        self._log_element_action("click", id_, name, class_, tag)

        element = self.element(id_, name, class_, tag)
        element.click()

        self.log_page()

    def submit(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            tag: Optional[str] = None) -> None:
        self._log_element_action("click", id_, name, class_, tag)

        element = self.element(id_, name, class_, tag)
        element.click()

        self.log_page()

    def type_(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            text: Optional[str] = None) -> None:
        element = self.element(id_, name, class_)
        element.send_keys(text)

    def screenshot(self, name: str):
        file_name = "%s.png" % (name)

        self.log.info("saving screenshot to '%s'" % (file_name))
        self.driver.get_screenshot_as_file(file_name)

    def save_source(self) -> None:
        self.log.info("write page source to page.html")
        with open("page.html", "w") as file_:
            file_.write(str(self.driver.page_source))

    def log_page(self) -> None:
        self.log.info(
            f"page title is {self.driver.title} ({self.driver.current_url})")
