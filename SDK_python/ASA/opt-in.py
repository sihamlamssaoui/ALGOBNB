# Copyright Cristian Lepore

# Receive an asset

import json
from algosdk import account, algod, mnemonic, transaction
from Utils.txn import wait_for_tx_confirmation

# Shown for demonstration purposes. NEVER reveal secret mnemonics in practice.
# Change these values with your mnemonics
# mnemonic1 = "PASTE your phrase for account 1"
# mnemonic2 = "PASTE your phrase for account 2"
# mnemonic3 = "PASTE your phrase for account 3"

mnemonic1 = "knock royal network goose trick filter credit engine phrase style inner cement wasp weasel scan comfort true jewel rally tuition man split wrong about theory"
mnemonic2 = "oak window face eager organ large virus idea slide mad glance material strike holiday know prevent seven chimney vivid love credit foam fame ability sock"
mnemonic3 = "trick physical cargo middle toy tennis benefit answer frame balance tuition outdoor record force bubble original club off school sound tail wealth husband abandon prize"
mnemonic4 = "cause input waste observe first someone neither exhaust napkin mesh zone purpose seed property bomb output response age fancy across grid kite consider ability vicious"

# For ease of reference, add account public and private keys to
# an accounts dict.
accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3, mnemonic4]:
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
print("Account 4 address: {}".format(accounts[4]['pk']))

# copy in your assetID
asset_id = (13256775)
# Check if asset_id is in account 3's asset holdings prior to opt-in
account_info = algod_client.account_info(accounts[4]['pk'])
holding = None
if 'assets' in account_info:
    holding = account_info['assets'].get(str(asset_id))

if not holding:
    # Get latest network parameters
    data = {
        "sender": accounts[4]['pk'],
        "fee": min_fee,
        "first": first,
        "last": last,
        "gh": gh,
        "receiver": accounts[3]["pk"],
        "amt": 0,
        "index": asset_id,
        "flat_fee": True
    }

# Use the AssetTransferTxn class to transfer assets and opt-in
txn = transaction.AssetTransferTxn(**data)

# Sign the transaction
stxn = txn.sign(accounts[4]['sk'])

txid = algod_client.send_transaction(stxn)
print(txid)

# Wait for the transaction to be confirmed
wait_for_tx_confirmation(algod_client, txid)

# Now check the asset holding for that account.
# This should now show a holding with a balance of 0.
account_info = algod_client.account_info(accounts[3]['pk'])
print(json.dumps(account_info['assets'][str(asset_id)], indent=4))
