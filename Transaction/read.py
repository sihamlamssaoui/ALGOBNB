# Copyright Cristian Lepore

# Read the transaction from the blockchain

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
import json, base64

# Connect to client
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

# Send the transaction
txid = 'AP3P7I4PXRQ6FUXGYORXJ2Y65D75HBLBWIOCDNG3BTVE2ITMK2YQ'
print("Successfully sent transaction with txID: {}".format(txid))

# Read the transaction from the blockchain
confirmed_txn = algod_client.pending_transaction_info(txid)
print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
print("Decoded note: {}".format(base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode()))
