from web3 import Web3
import json
import dotenv
import os
dotenv.load_dotenv()

# Connect to local blockchain
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))

# Replace this
CONTRACT_ADDRESS = "0x2f9E9142f5A74C30ad7852c9F42a1eE7f0EB58aB"

# Load ABI
with open("artifacts/contracts/TransactionLogger.sol/TransactionLogger.json") as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

PRIVATE_KEY = os.getenv("pvt_key")
ACCOUNT_ADDRESS = os.getenv("acc_addr")


def log_to_blockchain(user_id, amount, status, risk_score, data_hash):
    nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

    tx = contract.functions.logTransaction(
        user_id,
        int(amount),
        status,
        int(risk_score),
        data_hash
    ).build_transaction({
        "from": ACCOUNT_ADDRESS,
        "nonce": nonce,
        "gas": 800000,
        "gasPrice": w3.to_wei("10", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt.transactionHash.hex()