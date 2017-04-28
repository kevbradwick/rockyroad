_webdriver = None


def setup(webdriver):
    global _webdriver
    _webdriver = webdriver


def get_driver():
    global _webdriver
    return _webdriver