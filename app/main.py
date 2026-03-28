from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, engine
from . import models, schemas, crud
from .fraud_engine import calculate_risk
from .blockchain import log_to_blockchain
from .email_service import send_fraud_alert
from .utils import generate_tx_hash
from .verification import verify_transaction_integrity

# -------------------------------
# Create DB tables
# -------------------------------
models.Base.metadata.create_all(bind=engine)


# -------------------------------
# App Initialization
# -------------------------------
app = FastAPI(title="Fraud Detection + Blockchain API")


# -------------------------------
# CORS (for frontend)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Dependency (DB session)
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# 🚀 Create Transaction API
# -------------------------------
@app.post("/transaction", response_model=schemas.TransactionResponse)
def create_transaction(txn: schemas.TransactionCreate, db: Session = Depends(get_db)):

    # 🔹 Step 1: Fraud Detection
    risk_score, status, reasons = calculate_risk(
        db,
        txn.user_id,
        txn.amount,
        txn.ip_address
    )
    data_hash = generate_tx_hash(
        txn.user_id,
        txn.amount,
        status,
        risk_score
    )
    # 🔹 Step 2: Blockchain logging
    try:
        tx_hash = log_to_blockchain(
            txn.user_id,
            txn.amount,
            status,
            risk_score,
            data_hash
        )
    except Exception as e:
        print("Blockchain Error:", e)
        tx_hash = "BLOCKCHAIN_ERROR"

    # 🔹 Step 3: Save in DB
    result = crud.create_transaction(
        db,
        user_id=txn.user_id,
        amount=txn.amount,
        status=status,
        risk_score=risk_score,
        blockchain_tx=tx_hash,
        data_hash = data_hash
    )

    # 🔥 Step 4: Email alert (UPDATED)
    if status == "FRAUD":
        try:
            send_fraud_alert(
                user_id=txn.user_id,
                amount=txn.amount,
                risk_score=risk_score,
                status=status,
                reasons=reasons,
                tx_hash=tx_hash
            )
        except Exception as e:
            print("Email Error:", e)

    # 🔹 Step 5: Response
    return schemas.TransactionResponse(
        id=result.id,
        user_id=result.user_id,
        amount=result.amount,
        status=result.status,
        risk_score=result.risk_score,
        reasons=reasons,
        blockchain_tx=tx_hash
    )


# -------------------------------
# 📊 Get All Transactions API
# -------------------------------
@app.get("/transactions", response_model=list[schemas.TransactionDB])
def get_all_transactions(db: Session = Depends(get_db)):
    return crud.get_transactions(db)



@app.get("/verify/{tx_id}")
def verify(tx_id: int, db: Session = Depends(get_db)):
    return verify_transaction_integrity(db, tx_id)

# -------------------------------
# ❤️ Health Check
# -------------------------------
@app.get("/")
def root():
    return {"message": "Fraud Detection API is running 🚀"}