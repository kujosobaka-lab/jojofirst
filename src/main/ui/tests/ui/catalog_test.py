import pytest
from playwright.sync_api import Page
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps

@pytest.mark.ui
# подсчет карточек каталога
class TestCatalog:
    def test_count_catalog(self, page: Page):
       steps = CatalogSteps(page)
       steps.login('standard_user', 'secret_sauce')

       catalog_page = CatalogPage(page)
       assert steps.get_products_count() == 6, 'Количество товаров не равно 6'

    # сортировка карточек от A до Z
    def test_sorted_by_name(self, page: Page):
        steps = CatalogSteps(page)
        steps.login('standard_user', 'secret_sauce')

        steps.sort_items('az')
        assert steps.get_product_names() == sorted(steps.get_product_names()), 'Товары не отсортированы по наименованию A → Z'

        steps.sort_items('za')
        assert steps.get_product_names() == sorted(steps.get_product_names(), reverse=True), 'Товары не отсортированы по наименованию Z → A'

    # Сортировка по прайсу
    def test_sort_by_price(self, page: Page):
        steps = CatalogSteps(page)
        steps.login('standard_user', 'secret_sauce')

        # Сортировка по цене от low to high
        steps.sort_items("lohi")
        assert steps.get_product_prices() == sorted(steps.get_product_prices()), "Товары не отсортированы по цене low → high"

        # Сортировка по цене от high to low
        steps.sort_items('hilo')
        assert steps.get_product_prices() == sorted(steps.get_product_prices(), reverse=True), "Товары не отсортированы по цене high → low"

    # Добавление товара в корзину
    def test_add_to_cart(self, page: Page):
        steps = CatalogSteps(page)
        steps.login('standard_user', 'secret_sauce')

        steps.add_to_cart('Sauce Labs Bike Light')
        assert steps.get_cart_count() == 1, 'В корзину не добавлен товар или добавлено больше одного'

    # Удаление товара из корзины
    def test_add_and_remove_onesie(self, page: Page):
        step = CatalogSteps(page)
        step.login('standard_user', 'secret_sauce')

        step.add_to_cart('Sauce Labs Onesie')
        assert step.get_cart_count() == 1, 'В корзину не добавлен товар или добавлено больше одного'

        step.remove_from_cart('Sauce Labs Onesie')
        assert step.get_cart_count() == 0, 'В корзине остались товары'

    # Переход в карточку товара
    def test_product_details_onesie(self, page: Page):
        step = CatalogSteps(page)
        step.login('standard_user', 'secret_sauce')

        name, price, detail_name, detail_price = step.open_product_details('Sauce Labs Onesie')
        assert name == detail_name, 'Наименование карточки товара из каталога не совпадает с наименованием из деталей товара'
        assert price == detail_price, 'Цена карточки товара из каталога не совпадает с ценой из деталей товара'

    def test_product_details_fleece_jacket(self, page: Page):
        step = CatalogSteps(page)
        step.login('standard_user', 'secret_sauce')

        name, price, detail_name, detail_price = step.open_product_details('Sauce Labs Fleece Jacket')
        assert name == detail_name, 'Наименование карточки товара из каталога не совпадает с наименованием из деталей товара'
        assert price == detail_price, 'Цена карточки товара из каталога не совпадает с ценой из деталей товара'

    def test_remove_item_from_catalog(self, page: Page):
        step = CatalogSteps(page)
        step.login('standard_user', 'secret_sauce')

        step.remove_from_cart('Test.allTheThings() T-Shirt (Red)')





