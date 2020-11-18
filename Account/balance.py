# Copyright Cristian Lepore

# Check your balance to confirm the added funds.

from algosdk import account, mnemonic
from algosdk.v2client import algod

# Connect to client
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

# Substitute with your own passphrase.
passphrase = "tongue parent ginger trim upper card egg music sting merge wine hurry joke size leave volume siege juice sudden face scheme two okay abandon medal"

private_key = mnemonic.to_private_key(passphrase)
my_address = mnemonic.to_public_key(passphrase)
print("My address: {}".format(my_address))

account_info = algod_client.account_info(my_address)
print("Account balance: {} microAlgos".format(account_info.get('amount')))