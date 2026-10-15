from playwright.sync_api import Page, expect
from src.main.ui.pages.base_page import BasePage
from src.main.ui.utils.constants import URL

class LoginPage(BasePage):
    URL = URL.BASE

    def __init__(self, page: Page):
        super().__init__(page)
        self.error_message = page.locator("h3[data-test='error']")

    def open(self):
        '''Открываем страницу логина'''
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        '''Логинимся пользователем'''
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self) -> str:
        '''Вывод текста ошибки'''
        return self.error_message.inner_text()
    # page.goto('https://www.saucedemo.com/')  # открываем нужную страницу
    #
    # page.get_by_placeholder('Username').fill('standard_user')  # заполняем валидный логин
    # page.get_by_placeholder('Password').fill('secret_sauce')  # заполняем валидный пароль
    # page.locator('#login-button').click()  # кликаем по кнопке входа "Login"
    ...