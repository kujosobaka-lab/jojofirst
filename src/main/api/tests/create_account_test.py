# Позитивные: открытие одного счета (ROLE_USER)
# Негативный: создание более 2 счетов (ROLE_USER)

import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.models.user_table import User


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, db_session: Session, api_manager: ApiManager, create_user_data: CreateUserRequest):
        response = api_manager.user_steps.create_account(create_user_data)

        assert response.balance == 0, 'Счет создан с ненулевым балансом'

        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Аккаунт не создан, id аккаунта нет в БД'
        assert account_from_db.balance is not None, 'Поле баланса для созданного аккаунта отсутствует в БД'

    def test_create_accounts_maximum_accounts(self, db_session: Session, api_manager: ApiManager, create_user_data: CreateUserRequest):
        first_account = api_manager.user_steps.create_account(create_user_data)
        api_manager.user_steps.create_account(create_user_data)
        response = api_manager.user_steps.create_account_maximum(create_user_data)

        assert response.json()['error'] == 'User already has maximum number of accounts(2)', 'Для пользователя создано более двух аккаунтов'

        user_from_db = AccountCrudDb.get_account_by_id(db_session, first_account.id)
        accounts = AccountCrudDb.get_accounts_by_user_id(db_session, user_from_db.user_id)
        assert len(accounts) == 2, 'Создалось больше двух счетов'