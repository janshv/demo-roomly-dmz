# pages/components/field_component.py
import re
from playwright.sync_api import Locator, expect


class FieldComponent:
    def __init__(self, page, name: str):
        self.page = page
        self.root = page.locator(f'.field:has([name="{name}"])')
        self.input = self.root.locator(f'[name="{name}"]')
        self.error = self.root.locator('.field-error')

    def fill(self, value: str):
        self.input.fill(value)

    def select_option(self, value: str):
        self.input.select_option(value)

    def expect_error(self, text: str):
        expect(self.root).to_have_class(re.compile(r"\bhas-error\b"))
        expect(self.error).to_have_text(text)

    def expect_no_error(self):
        expect(self.root).not_to_have_class(re.compile(r"\bhas-error\b"))
        expect(self.error).to_be_empty()