# Позитивный: авторизация ROLE_ADMIN, авторизация ROLE_USER
# Негативный: авторизация с неверным логином

import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.user_login_request import UserLoginRequest


@pytest.mark.api
class TestLoginUser:
    def test_login_admin(self, db_session:Session, api_manager: ApiManager):
        login_user_request = UserLoginRequest(username='admin', password='123456')
        response = api_manager.admin_steps.user_login(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == 'ROLE_ADMIN'

        # проверка через БД кажется избыточной и бесполезной

    def test_login_user(self, api_manager, create_user_data):
        response = api_manager.admin_steps.user_login(create_user_data)

        assert create_user_data.username == response.user.username
        assert response.user.role == 'ROLE_USER'

    def test_login_credit(self, api_manager, create_credit_user_data):
        response = api_manager.admin_steps.user_login(create_credit_user_data)

        assert create_credit_user_data.username == response.user.username
        assert response.user.role == 'ROLE_CREDIT_SECRET'

    def test_login_missing_user(self,api_manager, create_user_missing_login_data):
        response = api_manager.admin_steps.user_login_missing_login(create_user_missing_login_data)
