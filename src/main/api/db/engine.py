# здесь будет движок sqlalchemy, который управляет соединениями с бд
# echo=False отключает выывод логов скл
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker # это фабрика сессий
from src.main.api.configs.config import Config

engine = create_engine(Config.fetch('dataBaseUrl'), echo=False)
SessionLocal = sessionmaker(bind=engine)