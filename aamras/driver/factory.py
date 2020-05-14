
from enum import Enum
from typing import Mapping, Optional, Type

from selenium.webdriver import (
    Firefox as FirefoxDriver, FirefoxOptions,
    Chrome as ChromeDriver, ChromeOptions
)
from selenium.webdriver.remote.webdriver import WebDriver

from ..util import LoggerMixin
from .driver import Driver

class DriverName(str, Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"

    def __str__(self):
        return self.value

class _SeleniumMapping:
    __slots__ = ("driver_type", "options_type")

    def __init__(self, driver_type: Type[WebDriver], options_type: Type):
        self.driver_type = driver_type
        self.options_type = options_type

_selenium_mapping: Mapping[DriverName, _SeleniumMapping] = {
    DriverName.CHROME: _SeleniumMapping(ChromeDriver, ChromeOptions),
    DriverName.FIREFOX: _SeleniumMapping(FirefoxDriver, FirefoxOptions)
}
def _driver_type_for(name: DriverName) -> Type[WebDriver]:
    return _selenium_mapping[name].driver_type

def _options_type_for(name: DriverName) -> Type:
    return _selenium_mapping[name].options_type

class DriverFactory(LoggerMixin):
    def create(
            self,
            driver_name: Optional[DriverName] = None) -> Driver:
        if not driver_name:
            driver = Driver(self._try_selenium_drivers())
        else:
            driver = Driver(self._get_selenium_driver(driver_name))

        return driver

    def _get_options(self, options_type) -> object:
        options = options_type()
        options.headless = True

        return options

    def _get_selenium_driver(self, driver_name: DriverName) -> WebDriver:
        driver_type = _driver_type_for(driver_name)
        options_type = _options_type_for(driver_name)

        options = options_type()
        options.headless = True

        return driver_type(options=options)

    def _try_selenium_drivers(self) -> WebDriver:
        exceptions = {}

        for driver_name in DriverName:
            try:
                driver = self._get_selenium_driver(driver_name)
                self.log.info(f"successfully initialized {driver_name} driver")

                return driver
            except (OSError, Exception) as e:
                exceptions[driver_name] = e

        self.log.error("unable to initialize WebDriver")
        for (driver_name, exception) in exceptions.items():
            self.log.error("%s trace:" % (driver_name))
            self.log.exception(exception)

        raise Exception("unable to initialize WebDriver")
