from src.main.api.db.models.account_table import Account
from sqlalchemy.orm import Session

class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        return db.query(Account).filter_by(id=account_id).first()

    # удаление аккаунта
    @staticmethod
    def delete_account(db: Session, account_id: int) -> None:
        account = db.query(Account).filter_by(id=account_id).first()
        if account:
            db.delete(account)
            db.commit() #делаем комит, чтобы сохранилось не только в состоянии сессии, а ВООБЩЕ

    # обновление баланса
    # @staticmethod
    # def update_balance(db: Session, account_id: int, balance: int) -> Account | None:
    #     return db.query(Account).filter_by(id=account_id).first()
    #     if account:
    #         account.balance += amount
    #         db.commit()
    #         db.refresh(account)
    #
    #     return account

    # посчитать количество аккаунтов
    @staticmethod
    def get_accounts_by_user_id(db: Session, user_id: int) -> List[Account] | None:
        account = db.query(Account).filter_by(user_id=user_id).all()
        return account