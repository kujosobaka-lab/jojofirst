# Позитивный: открытие кредита, когда 1 счет
# Негативные: запрос кредита для ROLE_USER, граничные условия на сумму кредита

import pytest
from requests import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest


@pytest.mark.api
class TestCreditRequest:
    # запрос кредита для ROLE_CREDIT_SECRET
    def test_credit_request(self, db_session: Session, api_manager: ApiManager, create_credit_user_data: CreateUserRequest, credit_request_data: CreditRequestRequest):
        response = api_manager.user_steps.credit_request(create_credit_user_data, credit_request_data)
        assert response.termMonths == credit_request_data.termMonths, 'Одобрен неверный срок кредита'
        assert response.balance == credit_request_data.amount, 'Баланс кредита не соответствует выданной сумме'

        transaction = TransactionCrudDb.get_credit_issuance(db_session, credit_request_data.accountId)
        assert transaction is not None, 'В БД не создалась транзакция выдачи кредита'
        assert transaction.transaction_type == 'credit_issuance', 'В БД записан неверный тип транзакции'

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session,response.creditId)
        assert credit_from_db.amount == credit_request_data.amount, 'В БД сохранена неверная сумма кредита'

    # запрос кредита для ROLE_USER
    def test_credit_request_invalid_role(self, db_session: Session, api_manager: ApiManager, create_user_data: CreateUserRequest, credit_request_data: CreditRequestRequest):
        response = api_manager.user_steps.credit_request_invalid_role(create_user_data, credit_request_data)
        assert response.status_code == 403, 'Пользователь с неверной ролью смог запросить кредит'

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, credit_request_data.accountId)
        assert credit_from_db is None, 'В БД создался кредит у пользователя без прав'

        transaction = TransactionCrudDb.get_credit_issuance(db_session, credit_request_data.accountId)
        assert transaction is None, 'В БД создалась транзакция выдачи кредита у пользователя без прав'

    # граничные условия на сумму кредита
    @pytest.mark.parametrize(
        'amount',
        [
            (-5000),
            (4999.99),
            (15001)
        ]
    )
    def test_credit_request_invalid_amount(self,
                                           db_session: Session,
                                           api_manager: ApiManager,
                                           create_credit_user_data: CreateUserRequest,
                                           create_credit_account_data:CreditRequestRequest,
                                           amount: float):
        request = CreditRequestRequest(
            accountId=create_credit_account_data.id,
            amount=amount,
            termMonths=12
        )
        response = api_manager.user_steps.credit_request_invalid_amount(create_credit_user_data, request)
        # ассерт на апи кажется избыточным
        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session,request.accountId)
        assert credit_from_db is None,  f'В БД создался кредит с некорректной суммой {amount}'

        transaction = TransactionCrudDb.get_credit_issuance(db_session, request.accountId)
        assert transaction is None, f'В БД создалась транзакция выдачи кредита с некорректной суммой {amount}'





















