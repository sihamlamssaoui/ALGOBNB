# Copyright Cristian Lepore

# Transfer asset

import json
from algosdk import account, algod, mnemonic, transaction

# Shown for demonstration purposes. NEVER reveal secret mnemonics in practice.
# Change these values with your mnemonics
# mnemonic1 = "PASTE your phrase for account 1"
# mnemonic2 = "PASTE your phrase for account 2"
# mnemonic3 = "PASTE your phrase for account 3"

mnemonic1 = "portion never forward pill lunch organ biology weird catch curve isolate plug innocent skin grunt bounce clown mercy hole eagle soul chunk type absorb trim"
mnemonic2 = "place blouse sad pigeon wing warrior wild script problem team blouse camp soldier breeze twist mother vanish public glass code arrow execute convince ability there"
mnemonic3 = "image travel claw climb bottom spot path roast century also task cherry address curious save item clean theme amateur loyal apart hybrid steak about blanket"

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
asset_id = (13168960)

# Destroy Asset
# With all assets back in the creator's account,
# the manager (Account 1) destroys the asset.

data = {
    "sender": accounts[1]['pk'],
    "fee": min_fee,
    "first": first,
    "last": last,
    "gh": gh,
    "index": asset_id,
    "strict_empty_address_check": False,
    "flat_fee": True
}

txn = transaction.AssetConfigTxn(**data)

# Sign transaction
stxn = txn.sign(accounts[2]['sk'])

txid = algod_client.send_transaction(stxn)
print(txid)

# Utility function to wait for a transaction to be confirmed by network
def wait_for_tx_confirmation(txid):
   last_round = algod_client.status().get('lastRound')
   while True:
       txinfo = algod_client.pending_transaction_info(txid)
       if txinfo.get('round') and txinfo.get('round') > 0:
           print("Transaction {} confirmed in round {}.".format(
               txid, txinfo.get('round')))
           break
       else:
           print("Waiting for confirmation...")
           last_round += 1
           algod_client.status_after_block(last_round)

# Wait for the transaction to be confirmed
wait_for_tx_confirmation(txid)

# This should raise an exception since the asset was deleted.
try:
    asset_info = algod_client.asset_info(asset_id)
except Exception as e:
    print(e)
