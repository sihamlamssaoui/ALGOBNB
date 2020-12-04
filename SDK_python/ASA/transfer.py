# Copyright Cristian Lepore

# Transfer asset

import json
from algosdk import account, algod, mnemonic, transaction
from Utils.txn import wait_for_tx_confirmation

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

# transfer asset of 10 from account 1 to account 3
data = {
    "sender": accounts[3]['pk'],
    "fee": min_fee,
    "first": first,
    "last": last,
    "gh": gh,
    "receiver": accounts[4]["pk"],
    "amt": 0,
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
print(json.dumps(account_info['assets'][str(asset_id)], indent=4))
