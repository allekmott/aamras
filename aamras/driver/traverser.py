"""DOM tree traversal functionality."""

from typing import Callable, List, Optional

from selenium.webdriver.remote.webdriver import WebElement

def _attr_filter(attr: str, value: str) -> Callable[[WebElement], bool]:
    """Construct an HTML attribute-based filter predicate.

    Only elements having the provided attribute set to the provided value will
    pass the filter.

    :param attr: name of attribute to filter by
    :param value: value of attr to filter by
    """
    def filter_(element: WebElement) -> bool:
        return bool(element.get_attribute(attr) == value)

    return filter_

def _tag_filter(tag: str) -> Callable[[WebElement], bool]:
    """Construct a HTML tag-based filter predicate.

    Only elements having the provided tag will pass the filter.

    :param tag: tag to filter by
    """
    def filter_(element: WebElement) -> bool:
        return bool(element.tag_name == tag)

    return filter_

def _class_filter(class_: str) -> Callable[[WebElement], bool]:
    """Construct a CSS class-based filter predicate.

    Only elements having the provided class will pass the filter.

    :param class_: name of class to filter by
    """
    def filter_(element: WebElement) -> bool:
        classes = element.get_attribute("class").split(" ")
        return class_ in classes

    return filter_

class Traversable:
    def find_elements_by_id(self, id: str) -> List[WebElement]:
        pass

    def find_elements_by_name(self, name: str) -> List[WebElement]:
        pass

    def find_elements_by_tag_name(self, tag: str) -> List[WebElement]:
        pass

    def find_elements_by_class_name(self, class_: str) -> List[WebElement]:
        pass

    def find_element_by_id(self, id: str) -> WebElement:
        pass

    def find_element_by_name(self, name: str) -> WebElement:
        pass

    def find_element_by_tag_name(self, tag: str) -> WebElement:
        pass

    def find_element_by_class_name(self, class_str) -> WebElement:
        pass

class Traverser:
    """DOM traverser for selenium elements/drivers."""
    dom_root: Traversable

    def __init__(self, dom_root: Traversable):
        self.dom_root = dom_root

    def elements(
            self,
            id_: Optional[str] = None,
            name: Optional[str] = None,
            class_: Optional[str] = None,
            tag: Optional[str] = None) -> List[WebElement]:
        """Search the DOM for elements matching provided criteria.

        At least one criterion must be provided.

        :param id_: HTML id attribute value to filter by
        :param name: HMTL name attribute value to filter by
        :param class_: CSS class to filter by
        :param tag: HTML tag name to filter by
        :returns: List of WebElements matching criteria
        :raises AssertionError: if no criterion is provided
        """
        identifiers_defined = list(filter(bool, [id_, name, class_, tag]))
        assert identifiers_defined, \
            "At least one of id_, name, class_, or tag must be defined"

        filters: List[Callable[[WebElement], bool]] = []
        matches: List[WebElement] = []

        if id_:
            matches.extend(self.dom_root.find_elements_by_id(id_))
            filters.append(_attr_filter("id", id_))

        if name:
            matches.extend(self.dom_root.find_elements_by_name(name))
            filters.append(_attr_filter("name", name))

        if class_:
            matches.extend(self.dom_root.find_elements_by_class_name(class_))
            filters.append(_class_filter(class_))

        if tag:
            matches.extend(self.dom_root.find_elements_by_tag_name(tag))
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
        """Serch the DOM for a single element matching provided criteria.

        Only one criterion should be provided.

        :param id_: HTML id attribute value to filter by
        :param name: HMTL name attribute value to filter by
        :param class_: CSS class to filter by
        :param tag: HTML tag name to filter by
        :returns: WebElement matching criteria or None if no matches were found
        :raises AssertionError: if no or more than one criterion is provided
        :raises selenium.webdriver.common.exceptions.NoSuchElementException: if
            no matching element is found
        """
        identifiers_defined = list(filter(bool, [id_, name, class_, tag]))
        assert len(identifiers_defined) == 1, \
            "Either id_, name, class_, or tag must be defined"

        if id_:
            match = self.dom_root.find_element_by_id(id_)
        elif name:
            match = self.dom_root.find_element_by_name(name)
        elif class_:
            match = self.dom_root.find_element_by_class_name(class_)
        elif tag:
            match = self.dom_root.find_element_by_tag_name(tag)

        return match
