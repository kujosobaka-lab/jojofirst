import allure
from playwright.sync_api import Page, expect
from src.main.ui.pages.checkout_page import CheckoutPage

class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout = CheckoutPage(page)

    @allure.step('Открываем страницу заказа')
    def open(self):
        self.checkout.open()
        return self

    @allure.step('Заполшняем данные получателя')
    def first_checkout(self, first_name: str, last_name: str, postal_code: int):
        self.checkout.first_checkout(first_name=first_name, last_name=last_name, postal_code=postal_code)
        return self

    @allure.step('Нажимаем финиш')
    def finish_checkout(self):
        self.checkout.finish_checkout()
        return self

    @allure.step('Получаем сообщение об ошибке при заполнении данных получателя')
    def get_error_text(self):
        return self.checkout.get_error_text()

    @allure.step('Получаем сообщение об успешном формировании заказа')
    def get_success_text(self):
        return self.checkout.get_success_text()

    @allure.step('...')
    def get_item_total(self) -> float:
        return self.checkout.get_item_total()

    @allure.step('...')
    def get_item_total_after_continue(self) -> float:
        return self.checkout.get_item_total_after_continue()