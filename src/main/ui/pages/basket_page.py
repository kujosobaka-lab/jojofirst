from playwright.sync_api import Page, expect
from src.main.ui.conftest import page
from src.main.ui.utils.constants import URL


class BasketPage:
    URL = URL.CART

    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.locator('.shopping_cart_link')
        self.item_cards = page.locator('.cart_item')
        self.checkout_button = page.locator('.checkout_button ')
        self.error_message = page.locator('[data-test="error"]')

    # --- Навигация ---
    def open(self):
        '''Переход в корзину через иконку'''
        self.cart_link.click()
        self.item_cards.first.wait_for(state='visible')

    def checkout(self):
        '''Нажать Checkout и перейти на страницу оформления заказа'''
        self.checkout_button.click()

    # --- Удаление товара из конзины---
    def remove_item(self, product_name: str):
        card = self.item_cards.filter(has_text=product_name)
        button = card.locator('button') # кнопка Remove
        button.click()

    # --- Проверки ---
    def expect_item_in_cart(self, product_name: str):
        '''Проверяем что в корзине лежит нужный товар'''
        card = self.item_cards.filter(has_text=product_name)
        expect(card).to_be_visible()

    def expect_item_not_in_cart(self, product_name: str):
        '''Проверяем что товара нет в корзине'''
        card = self.item_cards.filter(has_text=product_name)
        expect(card).to_be_not_visible()

    def get_item_names(self) -> list[str]:
        '''Возвращает список названий всех товаров в корзине'''
        return self.item_cards.locator('.inventory_item_name').all_text_contents()

    def get_item_prices(self) -> list[float]:
        '''Возвращает список цен всех товаров в корзине'''
        prices_text = self.item_cards.locator('.inventory_item_price').all_text_contents()
        return [float(p.replace('$', '')) for p in prices_text]

    def get_items_total_price(self) -> float:
        '''Возвращает полную цену товаров'''
        prices_text = self.item_cards.locator(".inventory_item_price").all_text_contents()
        return sum(float(p.replace("$", "")) for p in prices_text)