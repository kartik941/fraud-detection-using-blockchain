import hashlib

def generate_tx_hash(user_id, amount, status, risk_score):
    data = f"{user_id}-{amount}-{status}-{risk_score}"
    return hashlib.sha256(data.encode()).hexdigest()