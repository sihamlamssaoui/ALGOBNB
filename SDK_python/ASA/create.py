# Copyright Cristian Lepore

# Create an asset

import json
from algosdk import account, algod, mnemonic, transaction
from Utils.txn import wait_for_tx_confirmation

mnemonic1 = "delay lawsuit ladder silly parrot system treat save speak business sheriff brand cave hole churn shy eternal civil fix mother attitude employ canyon absorb biology"
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

# Configure fields for creating the asset.
# Account 1 creates an asset called latinum and sets Account 2 as the manager, reserve, freeze, and clawback address.
data = {
    "sender": accounts[1]['pk'],
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

# Sign with secret key of creator
stxn = txn.sign(accounts[1]['sk'])

# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(stxn)
print("Transaction ID = ", txid)

# Wait for the transaction to be confirmed
wait_for_tx_confirmation(algod_client, txid)

try:
    # Pull account info for the creator
    account_info = algod_client.account_info(accounts[1]['pk'])
    # Get max asset ID
    asset_id = max(
        map(lambda x: int(x), account_info.get('thisassettotal').keys()))
    print("Asset ID: {}".format(asset_id))
    print(json.dumps(account_info['thisassettotal'][str(asset_id)], indent=4))
except Exception as e:
    print(e)
