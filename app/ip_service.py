import requests
import dotenv
dotenv.load_dotenv()
import os

Api_KEY = os.getenv("api_key")

def check_ip(ip):
    try:
        url = f"https://ipqualityscore.com/api/json/ip/{Api_KEY}/{ip}"
        response = requests.get(url)
        data = response.json()
        return {
            "fraud_score": data.get("fraud_score", 0),
            "proxy": data.get("proxy", False),
            "country": data.get("country_code", "Unknown"),
            "success": data.get("success", False)
        }
    except Exception as e:
        print("IP API Error:", e)
        return {
            "fraud_score": 0,
            "proxy": False,
            "country": "Unknown",
            "success": False
        }