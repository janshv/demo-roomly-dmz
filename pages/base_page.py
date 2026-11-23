# pages/base_page.py
class BasePage:
    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self):
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        return self