from datetime import datetime
from app.ip_service import check_ip
from . import models


# -------------------------------
# Time check
# -------------------------------
def is_night_time():
    hour = datetime.now().hour
    return 2 <= hour <= 5


# -------------------------------
# 🔹 Get user average from DB
# -------------------------------
def get_user_avg_from_db(db, user_id):
    txns = (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == user_id)
        .all()
    )

    if len(txns) == 0:
        return None

    return sum(t.amount for t in txns) / len(txns)


# -------------------------------
# 🔹 Get transaction count
# -------------------------------
def get_user_txn_count(db, user_id):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == user_id)
        .count()
    )


# -------------------------------
# 🔥 Daily anomaly detection
# -------------------------------
def detect_daily_anomaly(db, user_id):
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)

    # 🔹 Past transactions (exclude today)
    past_txns = (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == user_id)
        .filter(models.Transaction.timestamp < today_start)
        .all()
    )

    if len(past_txns) < 3:
        return 0, None

    historical_avg = sum(t.amount for t in past_txns) / len(past_txns)

    # 🔹 Today's transactions
    today_txns = (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == user_id)
        .filter(models.Transaction.timestamp >= today_start)
        .all()
    )

    today_total = sum(t.amount for t in today_txns)
    today_count = len(today_txns)

    # 🔥 Detection logic
    if today_count >= 5 and today_total > 8 * historical_avg:
        return 50, "High daily transaction spike (FRAUD)"

    elif today_count >= 3 and today_total > 5 * historical_avg:
        return 30, "Unusual daily transaction volume (SUSPICIOUS)"

    return 0, None


# -------------------------------
# 🚀 MAIN FRAUD ENGINE
# -------------------------------
def calculate_risk(db, user_id, amount, ip_address):

    risk = 0
    reasons = []

    # 🔹 Rule 1: High transaction amount
    if amount > 50000:
        risk += 30
        reasons.append("High transaction amount")

    # 🔹 Rule 2: Night transaction
    if is_night_time():
        risk += 15
        reasons.append("Transaction at unusual time")

    # 🔹 Behavior check (DB-based)
    txn_count = get_user_txn_count(db, user_id)
    avg = get_user_avg_from_db(db, user_id)

    if txn_count >= 5 and avg:
        if amount > 5 * avg:
            risk += 40
            reasons.append("Amount significantly higher than user average")


    # 🔥 Daily anomaly detection
    extra_risk, reason = detect_daily_anomaly(db, user_id)

    if extra_risk > 0:
        risk += extra_risk
        reasons.append(reason)

    # 🔹 External IP check
    try:
        ip_data = check_ip(ip_address)

        if ip_data.get("success"):
            risk += ip_data.get("fraud_score", 0)

            if ip_data.get("proxy"):
                risk += 20
                reasons.append("IP is proxy/VPN")

            if ip_data.get("country") != "IN":
                risk += 25
                reasons.append(f"Foreign transaction ({ip_data.get('country')})")
        else:
            reasons.append("IP check failed")

    except Exception:
        reasons.append("IP check error")

    # 🔹 Final decision
    if risk < 40:
        status = "APPROVED"
    elif risk < 70:
        status = "SUSPICIOUS"
    else:
        status = "FRAUD"

    return risk, status, reasons