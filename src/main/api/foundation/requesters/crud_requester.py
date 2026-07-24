from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
from requests import Response
from src.main.api.configs.config import Config
import requests


class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel]) -> BaseModel | Response:
        body = model.model_dump() if model is not None else ''

# тут есть базовый урл и любой эндпоинт
        response = requests.post(
            url=f'{Config.fetch('backendUrl')}{self.endpoint.value.url}',
            headers=self.request_spec,
            json=body
        )
        self.response_spec(response)
        return response

    def delete(self, user_id: int) -> BaseModel | Response:
        response = requests.delete(
            url=f'{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response