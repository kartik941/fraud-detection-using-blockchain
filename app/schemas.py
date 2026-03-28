from pydantic import BaseModel
from typing import List


# 🔹 Input Model
class TransactionCreate(BaseModel):
    user_id: str
    amount: float
    ip_address: str


# 🔹 DB Model (internal use)
class TransactionDB(BaseModel):
    id: int
    user_id: str
    amount: float
    status: str
    risk_score: float
    data_hash: str

    class Config:
        orm_mode = True


# 🔹 API Response Model (final output)
class TransactionResponse(BaseModel):
    id: int
    user_id: str
    amount: float
    status: str
    risk_score: float
    reasons: List[str]
    blockchain_tx: str