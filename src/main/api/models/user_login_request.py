from src.main.api.models.base_model import BaseModel

# модель пидантика. когда будет много моделей, может быть какая-то новая зависимость,
# лучше сделать для бейс отдельную модель и наследовать от неё
class UserLoginRequest(BaseModel):
    username: str
    password: str