from src.main.api.db.models.transaction_table import Transaction
from sqlalchemy.orm import Session

class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(id=transaction_id).first()

    @staticmethod
    def get_transfer(db: Session, from_account_id: int, to_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                transaction_type='transfer'
            ).order_by(Transaction.id.desc()).first()

    @staticmethod
    def get_deposit(db: Session, to_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(
                to_account_id=to_account_id,
                transaction_type='deposit'
            ).order_by(Transaction.id.desc()).first()

    @staticmethod
    def get_credit_issuance(db_session: Session, account_id: int):
        return db_session.query(Transaction).filter(Transaction.to_account_id == account_id, Transaction.transaction_type == 'credit_issuance').first()

    @staticmethod
    def get_credit_repayment(db: Session, credit_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(credit_id=credit_id,transaction_type='credit_repayment').first()