# factories/page_factory.py
from pages.booking_page import BookingPage


class PageFactory:
    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url

    def booking_page(self) -> BookingPage:
        return BookingPage(self.page, self.base_url).open()