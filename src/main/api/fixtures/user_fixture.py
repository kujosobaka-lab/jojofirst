import pytest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest

# для роли ROLE_USER
@pytest.fixture
def create_user_data(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_user_missing_login_data(create_user_data):
    create_user_data.username = "not_existing_user"
    return create_user_data

@pytest.fixture
def create_account_data(api_manager, create_user_data):
    return api_manager.user_steps.create_account(create_user_data)

@pytest.fixture
def deposit_account_data(create_account_data):
    amount = 1000 #надо будет сделать генератор
    return DepositAccountRequest(
        accountId=create_account_data.id,
        amount=amount
    )

@pytest.fixture
def deposit_account_nonid_data(create_account_data):
    amount = 1000
    return DepositAccountRequest(
        accountId=1_1,
        amount=amount
    )

# создание двух счетов
@pytest.fixture
def create_several_account_data(api_manager, create_user_data):
    first_account = api_manager.user_steps.create_account(create_user_data)
    second_account = api_manager.user_steps.create_account(create_user_data)
    return first_account, second_account

# пополнение первого счета
@pytest.fixture
def transfer_deposit_data(create_several_account_data):
    first_account, second_account = create_several_account_data
    return DepositAccountRequest(
        accountId=first_account.id,
        amount=1100
    )

# для перевода
@pytest.fixture
def transfer_account_data(create_several_account_data):
    first_account, second_account = create_several_account_data
    return TransferAccountRequest(
        fromAccountId=first_account.id,
        toAccountId=second_account.id,
        amount=500
    )

@pytest.fixture
def transfer_account_invalid_amount_data(create_several_account_data, transfer_deposit_data):
    first_account, second_account = create_several_account_data
    return TransferAccountRequest(
        fromAccountId=first_account.id,
        toAccountId=second_account.id,
        amount=(transfer_deposit_data.amount + 100)
    )

# для роли ROLE_CREDIT_SECRET
@pytest.fixture
def create_credit_user_data(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = 'ROLE_CREDIT_SECRET'
    print(user_request.role)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_credit_account_data(api_manager, create_credit_user_data):
    return api_manager.user_steps.create_credit_account(create_credit_user_data)

@pytest.fixture
def credit_request_data(api_manager, create_credit_account_data): # ничего не отправляет, просто создает объект
   return CreditRequestRequest(
       accountId=create_credit_account_data.id,
       amount=5000,
       termMonths=12
   )

@pytest.fixture
def credit_response_data(api_manager, create_credit_user_data, credit_request_data): # должен отправить запрос, чтобы получить его данные
    return api_manager.user_steps.credit_request(create_credit_user_data, credit_request_data)

@pytest.fixture
def credit_repay_data(api_manager, credit_response_data):
    return CreditRepayRequest(
        creditId=credit_response_data.creditId,
        accountId=credit_response_data.id,
        amount=credit_response_data.amount
    )
@pytest.fixture
def credit_repay_invalid_amount_data(api_manager, credit_response_data):
    return CreditRepayRequest(
        creditId=credit_response_data.creditId,
        accountId=credit_response_data.id,
        amount=credit_response_data.amount + 100
    )