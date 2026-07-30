# Позитивный: пополнение одного счета (ROLE_USER)
# Негативный: ид счета не найден

import pytest
from requests import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.fixtures.db_fixture import db_session


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, db_session: Session, api_manager: ApiManager, create_user_data: CreateUserRequest, deposit_account_data: DepositAccountRequest):
        response = api_manager.user_steps.deposit_account(create_user_data, deposit_account_data)
        assert response.balance == deposit_account_data.amount, 'Счет не пополнен или пополнен на другую сумму'

        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)
        assert account_from_db.balance == deposit_account_data.amount, 'Счет пополнен на неверную сумму'
        assert account_from_db.id == deposit_account_data.accountId, 'Счет пополнен для другого аккаунта'

    # проверка на 404 ошибку (ид счета не найден)
    def test_deposit_account_nonid(self, db_session: Session, api_manager: ApiManager, create_user_data: CreateUserRequest, deposit_account_nonid_data: DepositAccountRequest):
        response = api_manager.user_steps.deposit_account_nonid(create_user_data, deposit_account_nonid_data)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, deposit_account_nonid_data.accountId)
        assert account_from_db is None, 'В БД найден счет с несуществующим id'

    # проверка на 404, но с параметрами
    @pytest.mark.parametrize(
        'account_id',
        ['1', '9999']
    )
    def test_deposit_account_invalid_id(self, db_session: Session, api_manager: ApiManager, create_user_data: CreateUserRequest, account_id: int):
        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=1000)
        response = api_manager.user_steps.deposit_account_nonid(create_user_data, deposit_account_request)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account_id)
        assert account_from_db is None, 'В БД найден счет с несуществующим id'

