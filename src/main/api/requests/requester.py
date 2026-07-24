# если будет много .реквестеров. то нужен один абстрактный, который
# будет заботиться о чем-то одном
from abc import ABC, abstractmethod
from typing import Dict, Callable
from src.main.api.models.base_model import BaseModel

# сам по себе абстрактный класс не будет реализовывать методы, но все. кто
# наследуется от него - будут
class Requester(ABC):
    def __init__(self, request_spec: Dict[str, str], response_spec: Callable):
        self.headers = request_spec['headers']
        self.base_url = request_spec['base_url']
        self.response_spec = response_spec

    @abstractmethod
    def post(self, model: BaseModel): # будем передавать BaseModel, т.к. все наши модели от неё наследуются
        # все модели, которые будут сюда приходить, они будут иметь типа Басе_модел
        ... # можно даже его не прописывать, конкретная реализация будет в наследниках
    #дальше для каждого тест можно создавать свои реквестеры