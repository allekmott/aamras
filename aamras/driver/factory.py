"""Driver factory/creation."""

from enum import Enum
from typing import Mapping, Optional, Type

from selenium.webdriver import (
    Firefox as FirefoxDriver, FirefoxOptions,
    Chrome as ChromeDriver, ChromeOptions
)
from selenium.webdriver.remote.webdriver import WebDriver

from ..util import LoggerMixin
from .driver import Driver

class DriverType(str, Enum):
    """Common driver types."""
    CHROME = "chrome"
    FIREFOX = "firefox"

    def __str__(self):
        return self.value

class _SeleniumMapping:
    """Data structure housing Selenium driver parameters"""
    __slots__ = ("driver_type", "options_type")

    def __init__(self, driver_type: Type[WebDriver], options_type: Type):
        self.driver_type = driver_type
        self.options_type = options_type

_webdriver_type_mapping: Mapping[DriverType, _SeleniumMapping] = {
    DriverType.CHROME: _SeleniumMapping(ChromeDriver, ChromeOptions),
    DriverType.FIREFOX: _SeleniumMapping(FirefoxDriver, FirefoxOptions)
}
def _webdriver_type(name: DriverType) -> Type[WebDriver]:
    return _webdriver_type_mapping[name].driver_type

def _options_type_for(name: DriverType) -> Type:
    return _webdriver_type_mapping[name].options_type

class DriverFactory(LoggerMixin):
    def create(self, driver_type: Optional[DriverType] = None) -> Driver:
        """Construct driver with the provided driver type.

        :param driver_type: type of driver to construct.
        """
        if not driver_type:
            driver = Driver(self._try_selenium_drivers())
        else:
            driver = Driver(self._get_selenium_driver(driver_type))

        return driver

    def _get_options(self, options_type) -> object:
        options = options_type()
        options.headless = True

        return options

    def _get_selenium_driver(self, driver_type: DriverType) -> WebDriver:
        """Construct a selenium WebDriver with the provided type.

        :param driver_type: type of driver to be created.
        """
        webdriver_type = _webdriver_type(driver_type)
        options_type = _options_type_for(driver_type)

        options = options_type()
        options.headless = True

        return webdriver_type(options=options)

    def _try_selenium_drivers(self) -> WebDriver:
        """Attempt to construct any driver type."""
        exceptions = {}

        for driver_type in DriverType:
            try:
                driver = self._get_selenium_driver(driver_type)
                self.log.info(f"successfully initialized {driver_type} driver")

                return driver
            except (OSError, Exception) as e:
                exceptions[driver_type] = e

        self.log.error("unable to initialize WebDriver")
        for (driver_type, exception) in exceptions.items():
            self.log.error("%s trace:" % (driver_type))
            self.log.exception(exception)

        raise Exception("unable to initialize WebDriver")

def create(driver_type: Optional[DriverType] = None):
    """Construct driver with the provided driver type.

    :param driver_type: type of driver to construct.
    """
    return DriverFactory().create(driver_type)
