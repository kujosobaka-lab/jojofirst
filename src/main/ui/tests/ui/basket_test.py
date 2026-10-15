import pytest
from playwright.sync_api import Page
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps
from src.main.ui.steps.basket_steps import BasketSteps

@pytest.mark.ui
# --- Добавление товара в корзину---
class TestBasket:
    def test_add_item_and_check_in_cart(self, page: Page):
        catalog_steps = CatalogSteps(page)
        basket_steps = BasketSteps(page)

        catalog_steps.login('standard_user', 'secret_sauce')
        catalog_steps.add_to_cart('Sauce Labs Backpack')

        basket_steps.open()
        assert "Sauce Labs Backpack" in basket_steps.get_item_names(), 'В корзине нет выбранного товара'

    # --- Добавление нескольких товаров в корзину ---
    def test_add_items_and_check_in_cart(self, page: Page):
        catalog_steps = CatalogSteps(page)
        basket_steps = BasketSteps(page)

        catalog_steps.login('standard_user', 'secret_sauce')
        catalog_steps.add_to_cart('Sauce Labs Fleece Jacket')
        catalog_steps.add_to_cart('Sauce Labs Bolt T-Shirt')

        basket_steps.open()
        items = basket_steps.get_item_names()
        assert "Sauce Labs Fleece Jacket" in basket_steps.get_item_names(), 'В корзине нет товара Sauce Labs Fleece Jacket'
        assert "Sauce Labs Bolt T-Shirt" in basket_steps.get_item_names(), 'В корзине нет товара Sauce Labs Bolt T-Shirt'

    # --- удаление из корзины одного товара ---
    def test_remove_item_from_cart(self, page: Page):
        catalog_steps = CatalogSteps(page)
        basket_steps = BasketSteps(page)

        catalog_steps.login('standard_user', 'secret_sauce')
        catalog_steps.add_to_cart('Sauce Labs Fleece Jacket')

        basket_steps.open()

        assert "Sauce Labs Fleece Jacket" in basket_steps.get_item_names(), 'В корзине нет товара Sauce Labs Fleece Jacket'

        basket_steps.remove_item('Sauce Labs Fleece Jacket')
        assert "Sauce Labs Fleece Jacket" not in basket_steps.get_item_names(), 'Из корзины не удален Sauce Labs Fleece Jacket'

    # --- удаление из товара двух товаров  Sauce Labs Backpack и Test.allTheThings() T-Shirt (Red)---
    def test_remove_items_from_cart(self, page: Page):
        catalog_steps = CatalogSteps(page)
        basket_steps = BasketSteps(page)

        catalog_steps.login('standard_user', 'secret_sauce')
        catalog_steps.add_to_cart('Test.allTheThings() T-Shirt (Red)')
        catalog_steps.add_to_cart('Sauce Labs Backpack')

        basket_steps.open()
        items = basket_steps.get_item_names()

        assert "Test.allTheThings() T-Shirt (Red)" in items, 'В корзине нет товара Test.allTheThings() T-Shirt (Red)'
        assert "Sauce Labs Backpack" in items, 'В корзине нет товара Sauce Labs Backpack'

        basket_steps.remove_item('Test.allTheThings() T-Shirt (Red)')
        basket_steps.remove_item('Sauce Labs Backpack')
        items = basket_steps.get_item_names()
        assert 'Sauce Labs Backpack' not in items, 'Из корзины не удален Sauce Labs Backpack'
        assert 'Test.allTheThings() T-Shirt (Red)' not in items, 'Из корзины не удален Test.allTheThings() T-Shirt (Red)'

    # самостоятельный Е2Е тест на покупку
    def test_checkout_multiple_items(self, page: Page):
        catalog_steps = CatalogSteps(page)
        basket_steps = BasketSteps(page)
        checkout_steps = CheckoutSteps(page)

        catalog_steps.login('standard_user', 'secret_sauce')
        catalog_steps.add_to_cart("Sauce Labs Fleece Jacket")
        catalog_steps.add_to_cart("Sauce Labs Bolt T-Shirt")

        basket_steps.open()
        items = basket_steps.get_item_names()

        assert "Sauce Labs Fleece Jacket" in items, 'В корзине нет товара Sauce Labs Fleece Jacket'
        assert "Sauce Labs Bolt T-Shirt" in items, 'В корзине нет товара Sauce Labs Bolt T-Shirt'

        basket_total = basket_steps.get_items_total_price()

        basket_steps.checkout()
        checkout_steps.first_checkout(first_name='Test', last_name='User', postal_code='12345')
        assert checkout_steps.get_item_total_after_continue() == pytest.approx(basket_total, 0.01)

        checkout_steps.finish_checkout()
        assert checkout_steps.get_success_text() == 'Thank you for your order!'

    # негативный тест на пропуск поля в форме Checkout
    def test_checkout_without_items(self, page: Page):
        catalog_steps = CatalogSteps(page)
        basket_steps = BasketSteps(page)
        checkout_steps = CheckoutSteps(page)

        catalog_steps.login('standard_user', 'secret_sauce')
        catalog_steps.add_to_cart("Sauce Labs Fleece Jacket")

        basket_steps.open()
        items = basket_steps.get_item_names()

        assert "Sauce Labs Fleece Jacket" in items, 'В корзине нет товара Sauce Labs Fleece Jacket'

        basket_steps.checkout()
        checkout_steps.first_checkout(first_name='Test', last_name='User', postal_code='')

        assert checkout_steps.get_error_text() == "Error: Postal Code is required"
