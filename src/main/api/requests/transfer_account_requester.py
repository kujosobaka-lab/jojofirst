import requests
from requests import Response

from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse
from src.main.api.requests.requester import Requester
from http import HTTPStatus


class TransferAccountRequester(Requester):
    def post(self, transfer_account_request: TransferAccountRequest) -> TransferAccountResponse | Response:
        url=f'{self.base_url}/account/transfer'
        response = requests.post(
            url=url,
            json=transfer_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        # там есть позитивные и негативные проверки и возвращать нужно то распакованное, то сырое, поэтому
        # поэтому делаем с проверкой. чтобы отдавало и так и так в зависимости от результата проверки
        if response.status_code == HTTPStatus.OK:
            return TransferAccountResponse(**response.json())
        return response