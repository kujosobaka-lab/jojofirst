from src.main.api.models.user_login_request import UserLoginRequest
import requests
from src.main.api.models.user_login_response import UserLoginResponse
from src.main.api.configs.config import Config


class RequestSpecs:
    # будут методы по возврату методов
    @staticmethod
    def base_headers():
        return {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }

    # метод для возвращения токена и добавления его к базовым хедерам
    @staticmethod
    def auth_headers(username: str, password: str):
        request = UserLoginRequest(username=username, password=password)
        response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=request.model_dump(),
            headers=RequestSpecs.base_headers()
        )
        if response.status_code == 200:
            response_data = UserLoginResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers['Authorization'] = f'Bearer {token}'
            return headers
        raise Exception('Failed to login')

    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers()