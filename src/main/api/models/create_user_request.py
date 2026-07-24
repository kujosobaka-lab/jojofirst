from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel
from typing import Annotated

class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationRule(regex=r'^[A-Za-z0-9]{3,15}$')]
    password: Annotated[str, CreationRule(regex=r'^[A-Z]{3}[a-z]{1}[0-9]{2}[!$_]{4}$')] # это регулярное вырежние, им мы устанавливаем правила, по которыми будут гнериться пароли. например больших буков 3, маленьких 1, цифр 2 и символов 4
    role: Annotated [str, CreationRule(regex=r'^ROLE_USER')]