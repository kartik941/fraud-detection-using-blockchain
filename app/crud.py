from sqlalchemy.orm import Session
from . import models

def create_transaction(db: Session, user_id: str, amount: float, status: str, risk_score: float, blockchain_tx: str = None, data_hash:str = None):
    txn = models.Transaction(
        user_id=user_id,
        amount=amount,
        status=status,
        risk_score=risk_score,
        blockchain_tx=blockchain_tx,
        data_hash = data_hash
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn

def get_transactions(db: Session):
    return db.query(models.Transaction).all()
