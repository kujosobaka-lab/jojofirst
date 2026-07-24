from http import HTTPStatus

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.requester import Requester
import requests


class CreateAccountRequester(Requester):
    def post(self, model=None) -> CreateAccountResponse:
        # обязаны там прописать модел=нон, т.к. наследуемся от реквестера, а там обязательно нужно это использовать)
        url=f'{self.base_url}/account/create'
        response = requests.post(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.CREATED:
            return CreateAccountResponse(**response.json())
        return response