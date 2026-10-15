import pytest
from playwright.sync_api import Page
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.catalog_steps import CatalogSteps

@pytest.mark.ui
class TestAuth:
    def test_auth(self, page: Page):
        steps = LoginSteps(page)
        steps.open_login_page().login('standard_user', 'secret_sauce')

        catalog_step = CatalogSteps(page)
        assert catalog_step.get_products_count() > 0, 'На странице не отобразились товары'

    def test_auth_locked_out_user(self, page:Page):
        steps = LoginSteps(page)
        steps.open_login_page().login('locked_out_user', 'secret_sauce')

        error_text = steps.login_page.get_error_text()
        assert page.url == LoginPage.URL, 'Ождиаем остаться на странице логина'
        assert 'locked out' in error_text, 'Ожидаем сообщение о заблокированном пользователе'

    def test_logout(self, page: Page):
        login = LoginSteps(page)
        catalog = CatalogSteps(page)

        login.open_login_page().login('standard_user', 'secret_sauce')

        catalog.logout()
        assert page.url == login.LOGIN_URL, 'Не выплонен возврат на страницу логина'

    def test_logout_visual_user(self, page: Page):
        login = LoginSteps(page)
        catalog = CatalogSteps(page)

        login.open_login_page().login('visual_user', 'secret_sauce')
        assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

        catalog.logout()
        assert page.url == login.LOGIN_URL, 'Не выплонен возврат на страницу логина'
