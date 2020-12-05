# Utility function to wait for a transaction to be confirmed by network
def wait_for_tx_confirmation(algod_client, txid):
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
