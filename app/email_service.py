import smtplib
from email.mime.text import MIMEText
import dotenv
import os
dotenv.load_dotenv()
EMAIL = os.getenv("from_email")
PASSWORD = os.getenv("app_pass")
TO_EMAIL = os.getenv("to_mail")


def send_fraud_alert(user_id, amount, risk_score, status, reasons, tx_hash):
    try:
        subject = "🚨 Fraud Alert Detected"

        etherscan_link = f"https://sepolia.etherscan.io/tx/{tx_hash}"

        body = f"""
🚨 FRAUD ALERT 🚨

User ID: {user_id}
Amount: ₹{amount}
Status: {status}
Risk Score: {risk_score}

Reasons:
{', '.join(reasons)}

Blockchain Transaction:
{tx_hash}

View on Etherscan:
{etherscan_link}
"""

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = TO_EMAIL

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)

        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email error:", e)