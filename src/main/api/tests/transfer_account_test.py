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

        assert response.fromAccountIdBalance == (transfer_deposit_data.amount - transfer_account_data.amount), 'Баланс счета-отправителя после перевода рассчитан неверно'

        transaction = TransactionCrudDb.get_transfer(db_session, transfer_account_data.fromAccountId, transfer_account_data.toAccountId)
        assert transaction.amount == transfer_account_data.amount, 'В БД сохранена неверная сумма перевода'
        assert transaction.transaction_type == 'transfer',  'В БД сохранен неверный тип транзакции'

        from_account = AccountCrudDb.get_account_by_id(db_session, transfer_account_data.fromAccountId)
        to_account = AccountCrudDb.get_account_by_id(db_session,transfer_account_data.toAccountId)

        assert from_account.balance == (transfer_deposit_data.amount - transfer_account_data.amount), 'Баланс счета отправителя изменился неверно'
        assert to_account.balance == transfer_account_data.amount, 'Баланс счета получателя изменился неверно'

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

        assert response.json()['error'] == 'Insufficient funds. Current balance: 1100.00, required: 1200.00', 'Не вернулось сообщение о недостаточном балансе'

        from_account = AccountCrudDb.get_account_by_id(db_session,transfer_account_invalid_amount_data.fromAccountId)
        to_account = AccountCrudDb.get_account_by_id(db_session,transfer_account_invalid_amount_data.toAccountId)
        transaction = TransactionCrudDb.get_transfer(db_session, transfer_account_invalid_amount_data.fromAccountId, transfer_account_invalid_amount_data.toAccountId)

        assert from_account.balance == transfer_deposit_data.amount, 'Баланс счета-отправителя изменился после неуспешного перевода'
        assert to_account.balance == 0, 'Баланс счета-получателя изменился после неуспешного перевода'
        assert transaction is None, 'В БД создалась транзакция после неуспешного перевода'