from sqlalchemy.orm import Session
from src.main.api.db.models.user_table import User


class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter_by(username=username).first()

    # создание пользователя иногда можно так готовить данные для тестов
    def create_user(db: Session, username: str, password: str, role: str) -> User:
        user = User(
            username=username,
            password=password,
            role=role
        )
        db.add(user) # объект добавлен, но ещё не сохранен
        db.commit() # изменения зафиксированы в бд
        db.refresh(db) # возвращает актуальные данные из бд
        return user