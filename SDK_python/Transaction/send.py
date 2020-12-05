# Copyright Cristian Lepore

# Prepare the transaction - no send

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction

# Connect to client
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

# Substitute with your own passphrase.
passphrase = "bring educate drift rally oblige benefit crush task lunar solar grief license mercy tribe pole divorce blur donkey august impulse shed knife crime able name"

# Check your balance
private_key = mnemonic.to_private_key(passphrase)
my_address = mnemonic.to_public_key(passphrase)
print("My address: {}".format(my_address))

account_info = algod_client.account_info(my_address)
print("Account balance: {} microAlgos".format(account_info.get('amount')))

# Construct the transaction
params = algod_client.suggested_params()

# Set you own fee
params.flat_fee = True
params.fee = 1000

# Set receiver
receiver = "YFXXOAHHJF2X7ASJ5DO2E2ZG3NRKHV4W2UTXOMWL5LWINQNEBVLPOZBZNM"
note = "Hello World".encode()

# Prepare an unsigned transaction
unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, 1000000, None, note)

# Sign the transaction
signed_txn = unsigned_txn.sign(mnemonic.to_private_key(passphrase))

# Send the transaction
txid = algod_client.send_transaction(signed_txn)
print("Successfully sent transaction with txID: {}".format(txid))
