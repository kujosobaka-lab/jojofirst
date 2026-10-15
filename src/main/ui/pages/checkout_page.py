from playwright.sync_api import Page, expect
from src.main.ui.utils.constants import URL

class CheckoutPage:
    URL = URL.CHECKOUT

    def __init__(self, page: Page):
         self.page = page
         self.first_name_input = page.locator('#first-name')
         self.last_name_input = page.locator('#last-name')
         self.postal_code_input = page.locator('[data-test="postalCode"]')
         self.continue_button = page.locator('[data-test="continue"]')
         self.error_massage = page.locator('[data-test="error"]')
         self.item_cards = page.locator('.inventory_item_name')
         self.item_total = page.locator('.summary_subtotal_label')
         self.tax = page.locator('.summary_tax_label')
         self.total = page.locator('.summary_total_label')
         self.finish_button = page.locator('#finish')
         self.success_message = page.locator('.complete-header')

    # --- Действия ---
    def open(self):
        '''Переход на страницу заказа'''
        self.checkout_button.click()

    def first_checkout(self, first_name, last_name, postal_code):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def finish_checkout(self):
        self.finish_button.click()

    # --- Методы для получения данных из тестов ---
    def get_error_text(self) -> str:
        return self.error_massage.inner_text()

    def get_success_text(self) -> str:
        return self.success_message.inner_text()

    def get_item_total(self) -> float:
        # текст вида 'Item total: $39.39'
        total_text = self.item_total.inner_text()
        return float(total_text.replace('Item total: $', ''))

    def get_item_total_after_continue(self) -> float:
        # ждем появление элемента
        expect(self.item_total).to_be_visible()
        total_text = self.item_total.inner_text()
        return float(total_text.replace('Item total: $', ''))
