"""Element wrapper/decorator."""

from typing import cast, List, Optional

from selenium.webdriver.remote.webelement import WebElement

from ..util import LoggerMixin
from .traverser import Traverser, Traversable

class ElementTraverserMixin:
    _traverser: Traverser
    dom_root: Traversable

    @property
    def traverser(self) -> Traverser:
        if not hasattr(self, "_traverser") or not self._traverser:
            self._traverser = Traverser(self.dom_root)

        return self._traverser

    def elements(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            tag: Optional[str] = None) -> "List[Element]":
        """Search DOM for elements matching provided criteria.

        See :meth:`Traverser.elements` for more documentation.

        :returns: List of Elements matching criteria
        """
        return list(map(
            Element,
            self.traverser.elements(id_, name, class_, tag)))

    def element(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            tag: Optional[str] = None) -> "Element":
        """Search DOM for single element matching provided criteria.

        See :meth:`Traverser.element` for more documentation.

        :returns: Element matching criteria"""
        return Element(self.traverser.element(id_, name, class_, tag))

class Element(LoggerMixin, ElementTraverserMixin):
    """Wrapper for selenium WebElement."""
    _element: WebElement

    def __init__(self, element: WebElement):
        self._element = element

    @property
    def dom_root(self):
        return self._element

    @property
    def tag(self) -> str:
        return cast(str, self._element.tag_name)

    @property
    def id(self) -> Optional[str]:
        return cast(Optional[str], self._element.get_attribute("id"))

    @property
    def class_(self) -> Optional[str]:
        return cast(Optional[str], self._element.get_attribute("class"))

    @property
    def name(self) -> Optional[str]:
        return cast(Optional[str], self._element.get_attribute("name"))

    @property
    def text(self) -> Optional[str]:
        return cast(Optional[str], self._element.text)

    @property
    def selected(self) -> bool:
        return bool(self._element.is_selected())

    @property
    def enabled(self) -> bool:
        return bool(self._element.is_enabled())

    @property
    def displayed(self) -> bool:
        return bool(self._element.is_displayed())

    @property
    def description(self) -> str:
        params = {
            "id": self.id,
            "name": self.name,
            "class": self.class_
        }

        attributes = " ".join(
            [f"{k}=\"{v}\"" for (k, v) in params.items() if v])
        return f"<{self.tag}{attributes and ' '}{attributes}>"

    def __repr__(self):
        return self.description

    def __str__(self):
        return self.description

    def _log_basic_action(self, action: str) -> None:
        self.log.info(f"{action} element {self}")

    def attribute(self, name: str) -> Optional[str]:
        return cast(Optional[str], self._element.get_attribute(name))

    def clear(self) -> None:
        """Clear element's text, if present."""
        self._log_basic_action("clear")
        self._element.clear()

    def click(self) -> None:
        """Click the element."""
        self._log_basic_action("click")
        self._element.click()

    def submit(self) -> None:
        """Submit the element."""
        self._log_basic_action("submit")
        self._element.submit()

    def type(self, text: Optional[str]) -> None:
        """Send text input to the element."""
        self.log.info(f"type '{text}' to element {self}")
        self._element.send_keys(text)

    def screenshot(self, file_path: str) -> None:
        """Save screenshot of element.

        :param file_path: path of file to save screenshot to
        """
        self.log.info(
            f"save screenshot of element {self} to {file_path}")
        self._element.screenshot(file_path)
