from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class WebElement:
    """
    WebElement
    
    A WebElement represents a single object on the web page. It could be
    anything node from the DOM.
    """
    _locator = None

    def __init__(self, element_id=None, css=None, xpath=None, class_name=None,
                 tag_name=None, link_text=None, partial_link_text=None):
        if element_id:
            self._locator = (By.ID, element_id,)
        elif css:
            self._locator = (By.CSS_SELECTOR, css,)
        elif xpath:
            self._locator = (By.XPATH, xpath,)
        elif class_name:
            self._locator = (By.CLASS_NAME, class_name,)
        elif tag_name:
            self._locator = (By.TAG_NAME, tag_name,)
        elif link_text:
            self._locator = (By.LINK_TEXT, link_text,)
        elif partial_link_text:
            self._locator = (By.PARTIAL_LINK_TEXT, partial_link_text,)
        else:
            raise RuntimeError('Elements can only be matched using element_id,'
                               'css, xpath, class_name or node_name')

    def __get__(self, instance, owner):
        """
        Provides access to the underlying WebElement
        
        :rtype: selenium.webdriver.remote.webelement.WebElement
        """
        by, locator = self._locator

        # add a timeout, this should be set by some configuration, for now it's
        # 1 second.
        WebDriverWait(instance.driver, 1000).until(
            lambda d: d.find_element(by, locator))

        return instance.driver.find_element(by, locator)


class WebElements(WebElement):

    def __get__(self, instance, owner):
        """
        
        :param instance: 
        :param owner: 
        :rtype: str
        :return: list
        """
        by, locator = self._locator

        # add a timeout, this should be set by some configuration, for now it's
        # 1 second.
        WebDriverWait(instance.driver, 1000).until(
            lambda d: d.find_element(by, locator))

        return instance.driver.find_elements(by, locator)

