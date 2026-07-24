import requests
from requests import Response

from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.requests.requester import Requester
from http import HTTPStatus


class CreditRequestRequester(Requester):
    def post(self, credit_request_request: CreditRequestRequest) -> CreditRequestResponse | Response:
        url=f'{self.base_url}/credit/request'
        response = requests.post(
            url=url,
            json=credit_request_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        # там есть позитивные и негативные проверки и возвращать нужно то распакованное, то сырое, поэтому
        # поэтому делаем с проверкой. чтобы отдавало и так и так в зависимости от результата проверки
        if response.status_code == HTTPStatus.CREATED:
            return CreditRequestResponse(**response.json())
        return response