# pages/booking_page.py
import re
from playwright.sync_api import expect
from pages.base_page import BasePage
from pages.components.field_component import FieldComponent


class BookingPage(BasePage):
    def __init__(self, page, base_url: str):
        super().__init__(page, base_url)
        self.room = FieldComponent(page, "room")
        self.date = FieldComponent(page, "date")
        self.start_time = FieldComponent(page, "startTime")
        self.end_time = FieldComponent(page, "endTime")
        self.participants = FieldComponent(page, "participants")
        self.name = FieldComponent(page, "name")
        self.email = FieldComponent(page, "email")
        self.submit_button = page.get_by_role("button", name="Забронировать")
        self.status = page.locator("#form-status")

    def fill_booking(
        self,
        *,
        room: str = "small",
        date: str | None = None,
        start_time: str = "10:00",
        end_time: str = "11:00",
        participants: str = "2",
        name: str = "Иван Иванов",
        email: str = "ivan@example.com",
    ):
        if room:
            self.room.select_option(room)
        if date:
            self.date.fill(date)
        self.start_time.fill(start_time)
        self.end_time.fill(end_time)
        self.participants.fill(participants)
        self.name.fill(name)
        self.email.fill(email)

    def submit(self):
        self.submit_button.click()

    def expect_success_contains(self, *parts: str):
        # 1) ждём, что статус вообще отрисовался и стал видимым
        expect(self.status).to_be_visible()
        # 2) проверяем success-сигнал через regex
        expect(self.status).to_have_class(re.compile(r"\bsuccess\b"))
        # 3) проверяем содержимое
        for part in parts:
            expect(self.status).to_contain_text(part)

    def expect_error_summary(self):
        expect(self.status).to_be_visible()
        expect(self.status).to_have_class(re.compile(r"\berror\b"))
        expect(self.status).to_contain_text("Проверьте, пожалуйста, заполнение формы.")