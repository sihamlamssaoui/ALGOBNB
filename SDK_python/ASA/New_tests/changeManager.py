# Copyright Cristian Lepore

# Create an asset

import json
from algosdk.v2client import algod
from algosdk import account, algod, mnemonic, transaction
from Utils.txn import wait_for_tx_confirmation
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn

mnemonic1 = "knock royal network goose trick filter credit engine phrase style inner cement wasp weasel scan comfort true jewel rally tuition man split wrong about theory"
mnemonic2 = "oak window face eager organ large virus idea slide mad glance material strike holiday know prevent seven chimney vivid love credit foam fame ability sock"

# For ease of reference, add account public and private keys to
# an accounts dict.
accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

# Use your own algod address and token if any different
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token, algod_address)

# The current manager(Account 2) issues an asset configuration transaction that assigns Account 1 as the new manager.
# Keep reserve, freeze, and clawback address same as before, i.e. account 2
params = algod_client.suggested_params()

# Get network params for transactions.
params = algod_client.suggested_params()
first = params.get("lastRound")
last = first + 1000
gen = params.get("genesisID")
gh = params.get("genesishashb64")
min_fee = params.get("minFee")

asset_id = 13255544;

"""
txn = AssetConfigTxn(
    sender=accounts[2]['pk'],
    sp=params,
    index=asset_id,
    manager=accounts[1]['pk'],
    reserve=accounts[2]['pk'],
    freeze=accounts[2]['pk'],
    clawback=accounts[2]['pk'])
"""

# Configure fields for creating the asset.
# Account 1 creates an asset called latinum and sets Account 2 as the manager, reserve, freeze, and clawback address.
data = {
    "sender": accounts[2]['pk'],
    "fee": min_fee,
    "first": first,
    "last": last,
    "gh": gh,
    "total": 1,
    "default_frozen": False,
    "unit_name": "REP",
    "asset_name": "Reputation",
    "manager": accounts[2]['pk'],
    "reserve": accounts[2]['pk'],
    "freeze": accounts[2]['pk'],
    "clawback": accounts[2]['pk'],
    "url": "/Documents/Reputation_asset.txt",
    "flat_fee": True,
    "decimals": 0
}

# Construct Asset Creation transaction
txn = transaction.AssetConfigTxn(**data)

# sign by the current manager - Account 2
stxn = txn.sign(accounts[2]['sk'])
txid = algod_client.send_transaction(stxn)
print(txid)

# Wait for the transaction to be confirmed
wait_for_tx_confirmation(algod_client, txid)
