import pytest
from src.main.api.db.engine import SessionLocal, engine

@pytest.fixture(scope="function") # function - чтобы каждый тест работал в рамках своей сессии и тринзакции и данные другу с другом не кокурировали и не затирались
def db_session():
    connection = engine.connect()
    transaction = connection.begin() # это контейнер операций с бд
    session = SessionLocal(bind=connection)
    try:
        yield session #всегда отдаем сессию
    finally:
        session.close() # всегда закрываем сессию
        transaction.rollback() # всегда откатываем изменения, которые внесли
        connection.close() # и всегда закрываем коннект