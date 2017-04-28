from selenium import webdriver
from rockyroad.elements import WebElement
from rockyroad import setup


class GithubPage:
    author = WebElement(css='span.author')
    project_name = WebElement(css='strong[itemprop="name"] a')


driver = webdriver.Chrome()
setup(driver)
driver.get('https://github.com/kevbradwick/rockyroad')

page = GithubPage()

assert page.author.text == 'kevbradwick'

driver.quit()