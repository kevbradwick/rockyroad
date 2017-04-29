from . import config


class PageObject:
    url = None

    def __init__(self):
        self.driver = config.get_driver()

    def visit(self):
        """Visit the page object's URL."""
        if not self.url:
            raise RuntimeError('No URL has been set for this page object')

        base_url = config.get_base_url()
        if base_url:
            self.driver.get(base_url + self.url)
        else:
            self.driver.get(self.url)
