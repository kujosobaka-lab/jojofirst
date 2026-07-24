import requests

from src.main.api.models.user_login_request import UserLoginRequest
from src.main.api.models.user_login_response import UserLoginResponse
from src.main.api.requests.requester import Requester
from requests import Response


class UserLoginRequester(Requester):
    # т.к. нет негативных тк на это, то добавили типизацию..
    # на случай появления негативных кейсов в типизацию добавили респонс
    def post(self, user_login_request: UserLoginRequest) -> UserLoginResponse | Response:
        url=f'{self.base_url}/auth/token/login'
        response=requests.post(
            url=url,
            json=user_login_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return UserLoginResponse(**response.json())
