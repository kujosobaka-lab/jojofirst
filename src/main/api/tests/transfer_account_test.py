import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest


# перевод с го счета на 2-й при условии что на 2-м счету изначально 0
@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(self,
                                    db_session:Session,
                                    api_manager: ApiManager,
                                    create_user_data: CreateUserRequest,
                                    create_several_account_data: CreateAccountResponse,
                                    transfer_deposit_data: TransferAccountRequest,
                                    transfer_account_data: TransferAccountRequest):
        api_manager.user_steps.deposit_account(create_user_data, transfer_deposit_data)
        response = api_manager.user_steps.transfer_account(create_user_data, transfer_account_data)
        expected_balance = round(transfer_deposit_data.amount - transfer_account_data.amount, 2)
        assert round(response.fromAccountIdBalance, 2) == expected_balance, 'Баланс счета-отправителя после перевода рассчитан неверно'

        transaction = TransactionCrudDb.get_transfer(db_session, transfer_account_data.fromAccountId, transfer_account_data.toAccountId)
        assert transaction.transaction_type == 'transfer',  'В БД сохранен неверный тип транзакции'

        from_account = AccountCrudDb.get_account_by_id(db_session, transfer_account_data.fromAccountId)
        assert round(from_account.balance, 2) == expected_balance, 'Баланс счета отправителя изменился неверно'


    # ПРОВЕРКА, что переводимая сумма меньше баланса на счету-1
    def test_transfer_account_invalid(self,
                                      db_session:Session,
                                      api_manager: ApiManager,
                                      create_user_data: CreateUserRequest,
                                      create_several_account_data: CreateAccountResponse,
                                      transfer_deposit_data: TransferAccountRequest,
                                      transfer_account_invalid_amount_data: TransferAccountRequest):
        api_manager.user_steps.deposit_account(create_user_data, transfer_deposit_data)
        response = api_manager.user_steps.transfer_account_invalid(create_user_data, transfer_account_invalid_amount_data)
        expected_error = (f"Insufficient funds. Current balance: {transfer_deposit_data.amount:.2f}, "f"required: {transfer_account_invalid_amount_data.amount:.2f}")
        assert response.json()['error'] == expected_error, 'Не вернулось сообщение о недостаточном балансе'

        transaction = TransactionCrudDb.get_transfer(db_session, transfer_account_invalid_amount_data.fromAccountId, transfer_account_invalid_amount_data.toAccountId)
        assert transaction is None, 'В БД создалась транзакция после неуспешного перевода'