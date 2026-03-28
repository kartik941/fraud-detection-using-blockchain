from .utils import generate_tx_hash
from . import models

def verify_transaction_integrity(db, tx_id):
    txn = db.query(models.Transaction).filter(models.Transaction.id == tx_id).first()

    if not txn:
        return {"verified": False, "message": "Transaction not found"}

    recalculated_hash = generate_tx_hash(
        txn.user_id,
        txn.amount,
        txn.status,
        txn.risk_score
    )

    if recalculated_hash == txn.data_hash:
        return {"verified": True}
    else:
        return {"verified": False}