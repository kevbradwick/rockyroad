from selenium import webdriver
from rockyroad.elements import WebElement, WebElements
from rockyroad.page import PageObject
from rockyroad import config


class GithubPage(PageObject):
    url = '/kevbradwick/rockyroad'
    _author = WebElement(css='span.author')
    _project_name = WebElement(css='strong[itemprop="name"] a')
    _links = WebElements(tag_name='a')
    _search_input = WebElement(css='form input[name="q"]')

    def search(self, term):
        self._search_input.send_keys(term)
        self._search_input.submit()


# create an instance of WebDriver
driver = webdriver.Chrome()

# make rockyroad aware of it
config.set_driver(driver)
config.set_base_url('http://github.com')

page = GithubPage()
page.visit()
page.search('selenium')
