# Copyright Cristian Lepore

# Transfer asset

import json
from algosdk import account, algod, mnemonic, transaction
from Utils.txn import wait_for_tx_confirmation

mnemonic1 = "bring educate drift rally oblige benefit crush task lunar solar grief license mercy tribe pole divorce blur donkey august impulse shed knife crime able name"
mnemonic2 = "bomb leisure human gasp ripple sea flavor stove limit vessel gift poverty catalog equip umbrella actor glimpse protect rice idea style polar survey about carbon"
mnemonic3 = "hamster spy moment silly source decade proof utility pond sweet whale select meadow stem liquid appear way belt oblige caught clarify provide end about calm"

# For ease of reference, add account public and private keys to
# an accounts dict.
accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

# Use your own algod address and token if any different
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token, algod_address)

# Get network params for transactions.
params = algod_client.suggested_params()
first = params.get("lastRound")
last = first + 1000
gen = params.get("genesisID")
gh = params.get("genesishashb64")
min_fee = params.get("minFee")

# Print the accounts
print("Account 1 address: {}".format(accounts[1]['pk']))
print("Account 2 address: {}".format(accounts[2]['pk']))
print("Account 3 address: {}".format(accounts[3]['pk']))

# copy in your assetID
asset_id = (13257610)

# transfer asset of 10 from account 1 to account 3
data = {
    "sender": accounts[3]['pk'],
    "fee": min_fee,
    "first": first,
    "last": last,
    "gh": gh,
    "receiver": accounts[1]["pk"],
    "amt": 1,
    "index": asset_id,
    "flat_fee": True
}

# Transfer the transaction
txn = transaction.AssetTransferTxn(**data)

# Sign the transaction
stxn = txn.sign(accounts[3]['sk'])

# Send transaction and print out information
txid = algod_client.send_transaction(stxn)
print(txid)

# Wait for the transaction to be confirmed
wait_for_tx_confirmation(algod_client, txid)

# The balance should now be 10.
account_info = algod_client.account_info(accounts[3]['pk'])
