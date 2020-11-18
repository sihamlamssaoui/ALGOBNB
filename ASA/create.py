# Copyright Cristian Lepore
# This file needs to create an asset

# Import libraries
from algosdk.v2client import algod
from algosdk import account, mnemonic

# Connect to the client
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

# Get network params for transactions before every transaction.
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True

# Account 1 creates an asset called latinum and
# sets Account 2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction

txn = AssetConfigTxn(
    sender=accounts[1]['pk'],
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="LATINUM",
    asset_name="latinum",
    manager=accounts[2]['pk'],
    reserve=accounts[2]['pk'],
    freeze=accounts[2]['pk'],
    clawback=accounts[2]['pk'],
    url="https://path/to/my/asset/details", 
    decimals=0)
# Sign with secret key of creator
stxn = txn.sign(accounts[1]['sk'])

# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(stxn)
print(txid)

# Wait for confirmation
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.

# Wait for the transaction to be confirmed
wait_for_confirmation(algod_client,txid)

try:
    # Pull account info for the creator
    # account_info = algod_client.account_info(accounts[1]['pk'])
    # get asset_id from tx
    # Get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, accounts[1]['pk'], asset_id)
    print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
except Exception as e:
    print(e)
