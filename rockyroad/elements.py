from . import get_driver


class WebElement:
    """
    WebElement
    
    A WebElement represents a single object on the web page. It could be
    anything node from the DOM.
    """
    _locator_type = None
    _locator_value = None
    _cached_element = None

    def __init__(self, element_id=None, css=None, xpath=None, class_name=None,
                 tag_name=None):
        if element_id:
            self._locator_type = 'find_element_by_id'
            self._locator_value = element_id
        elif css:
            self._locator_type = 'find_element_by_css_selector'
            self._locator_value = css
        elif xpath:
            self._locator_type = 'find_element_by_xpath'
            self._locator_value = xpath
        elif class_name:
            self._locator_type = 'find_element_by_class_name'
            self._locator_value = class_name
        elif tag_name:
            self._locator_type = 'find_element_by_tag_name'
            self._locator_value = tag_name
        else:
            raise RuntimeError('Elements can only be matched using element_id,'
                               'css, xpath, class_name or node_name')

    def _get_element(self):
        if self._cached_element:
            return self._cached_element

        driver = get_driver()
        method = getattr(driver, self._locator_type)
        self._cached_element = method(self._locator_value)
        return self._cached_element

    def tag_name(self):
        return self._get_element().tag_name()

    def text(self):
        return self._get_element().text()

    def click(self):
        return self._get_element().click()

    def submit(self):
        return self._get_element().submit()

    def clear(self):
        return self._get_element().clear()

    def get_property(self, name):
        return self._get_element().get_property(name)

    def get_attribute(self, name):
        return self._get_element().get_attribute(name)

    def is_selected(self):
        return self._get_element().is_selected()

    def is_enabled(self):
        return self._get_element().is_enabled()

    def send_keys(self, *args):
        return self._get_element().send_keys(*args)

    def is_displayed(self):
        return self._get_element().is_displayed()

    def size(self):
        return self._get_element().size()

    def location(self):
        return self._get_element().location()

    def rect(self):
        return self._get_element().rect()

    def screenshot_as_base64(self):
        return self._get_element().screenshot_as_base64()

    def screenshot_as_png(self):
        return self._get_element().screenshot_as_png()

    def screenshot(self, filename):
        return self._get_element().screenshot(filename)
