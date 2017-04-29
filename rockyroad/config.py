from selenium.webdriver.remote.webdriver import WebDriver

# a configured instance of WebDriver
_DRIVER_INSTANCE = None

# a base url that all page object's will use when the navigate() mathod is
# called.
_BASE_URL = None

# the number of seconds to wait while looking up an element before timeout
_ELEMENT_LOOKUP_TIMEOUT = 10


def set_driver(driver):
    """
    Set the instance of web driver to be used throughout the library.
    :param driver: 
    :return: 
    """
    if not isinstance(driver, WebDriver):
        raise RuntimeError('{} must be an instance of WebDriver'.format(driver))

    global _DRIVER_INSTANCE
    _DRIVER_INSTANCE = driver


def get_driver():
    global _DRIVER_INSTANCE
    if not isinstance(_DRIVER_INSTANCE, WebDriver):
        raise RuntimeError('An instance of WebDriver has not been configured, '
                           'please call set_instance() with a valid instance '
                           'of WebDriver')

    return _DRIVER_INSTANCE


def set_base_url(url: str):
    global _BASE_URL
    _BASE_URL = url


def get_base_url():
    global _BASE_URL
    return _BASE_URL
