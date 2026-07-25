# ДОДЕЛАТЬ МОДЕЛЯМИ ПОСЛЕДНИЕ МЕТОДЫ

import requests
import pytest
from requests import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay(self, db_session: Session, api_manager: ApiManager, create_credit_user_data: CreateUserRequest, credit_repay_data: CreditRepayRequest):
        response = api_manager.user_steps.credit_repay(create_credit_user_data, credit_repay_data)
        assert response.creditId == credit_repay_data.creditId, 'Погашен неверный кредит'
        assert response.amountDeposited == credit_repay_data.amount, 'Погашена неверная сумма кредита'

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, credit_repay_data.creditId)
        assert credit_from_db.balance == 0, 'Кредит погашен не полностью'

        transaction = TransactionCrudDb.get_credit_repayment(db_session, credit_repay_data.creditId)
        assert transaction.transaction_type == 'credit_repayment', 'В БД записан неверный тип транзакции'

# негативный на 422. пытаюсь закрыть кредит недостаточной суммой
    def test_credit_repay_insufficient_funds(self, db_session: Session, api_manager: ApiManager, create_credit_user_data: CreateUserRequest, credit_repay_invalid_amount_data: CreditRepayRequest):
        response = api_manager.user_steps.credit_repay_invalid_amount(create_credit_user_data, credit_repay_invalid_amount_data)

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, credit_repay_invalid_amount_data.creditId)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, credit_repay_invalid_amount_data.accountId)

        transaction = TransactionCrudDb.get_credit_repayment(db_session, credit_repay_invalid_amount_data.creditId)
        assert transaction is None, 'В БД создалась запись о погашении кредита после неуспешной операции'
        assert account_from_db.balance == credit_from_db.amount, 'Со счета списались деньги после неуспешного погашения'