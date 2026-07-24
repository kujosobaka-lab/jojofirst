from pydantic import BaseModel as BM

class BaseModel(BM): ...
# когда появится общая зависимость между моделями, её можно будет прописать здесь