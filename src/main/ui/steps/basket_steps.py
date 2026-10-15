import allure
from playwright.sync_api import Page, expect
from src.main.ui.pages.basket_page import BasketPage

class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page)

    @allure.step('Переходим на страницу корзины')
    def open(self):
        self.basket.open()
        return self

    @allure.step('Переходим на страницу оформления заказа - первый шаг')
    def checkout(self):
        self.basket.checkout()
        return self

    @allure.step('Удаляем товар из корзины: {product_name}')
    def remove_item(self, product_name: str):
        self.basket.remove_item(product_name)
        return self

    @allure.step('Поверяем, что в корзине находится товар: {product_name}')
    def expect_item_in_cart(self, product_name: str):
        return self.basket.expect_item_in_cart(product_name)

    @allure.step('Поверяем, что в корзине не находится товар: {product_name}')
    def expect_item_not_in_cart(self, product_name: str):
        return self.basket.expect_item_not_in_cart(product_name)

    @allure.step('Получаем список всех товаров в корзине')
    def get_item_names(self) -> list[str]:
        return self.basket.get_item_names()

    @allure.step('Получаем список всех цен в корзине')
    def get_item_prices(self) -> list[float]:
        return self.basket.get_item_prices()

    @allure.step('Получаем общую сумму товаров в корзине')
    def get_items_total_price(self) -> float:
        return self.basket.get_items_total_price()