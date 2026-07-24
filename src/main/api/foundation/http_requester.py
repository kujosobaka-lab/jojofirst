# будет отвечать за логику, которая была в реквестере и хранить всю инфу о реквест спецификации и о респонс спецификации
from src.main.api.foundation.endpoint import Endpoint
from typing import Dict, Callable

# и реквест-спеки будут хранить теперь только хедеры
class HttpRequester:
    def __init__(self, request_spec: Dict, endpoint: Endpoint, response_spec: Callable):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec