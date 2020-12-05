# ALGOBNB


## Create app
$ goal app create --creator YJL5XKI4Y36NLQLPRQ3YQU4G2NOT2IHJ6MHLYGIPHZNUDLOGLTA44NVF4I  --approval-prog airbnb.teal  --global-byteslices 16 --global-ints 16 --local-byteslices 0 --local-ints 0 --app-arg "addr:7BHXE46DOOVFEMIHB7KSWJUY4UWTRVE4L5WIVXLHVXQWOCBPRA7EWFLPKU" --app-arg "int:300000" --app-arg "int:100000" --app-arg "int:100000" --app-arg "str:1" --app-arg "str:22" --clear-prog airbnb_clear.teal -d ~/node/testnet

-return APP_ID

## Example scenario 1:

compile escrow_account.teal:
$ goal clerk compile escrow_account.teal
-return address

update app using the escrow address:
$ goal app update --app-id=13066667 --from YJL5XKI4Y36NLQLPRQ3YQU4G2NOT2IHJ6MHLYGIPHZNUDLOGLTA44NVF4I  --approval-prog airbnb.teal   --clear-prog airbnb_clear.teal --app-arg "addr:$ESCROW_ADDRESS" -d ~/node/testnet

call the stateful contract:
$ goal app call --app-id 13078399  --app-arg "str:send_h_deposit" --from=YJL5XKI4Y36NLQLPRQ3YQU4G2NOT2IHJ6MHLYGIPHZNUDLOGLTA44NVF4I  --out=unsignedtransaction1.tx -d ~/node/testnet

send amount to escrow account:
$ goal clerk send --from=YJL5XKI4Y36NLQLPRQ3YQU4G2NOT2IHJ6MHLYGIPHZNUDLOGLTA44NVF4I --to="REQS52LD2DTM5DURYDJ4VKLXXGBWEUJMMLPMWTTCEPJICV7M23ZN5DTCSU" --amount=100000 --out=unsignedtransaction2.tx -d ~/node/testnet

combine them: 
$ cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx

group them:
$ goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

sign them:
$ goal clerk sign -i groupedtransactions.tx -o signout.tx -d ~/node/testnet

execute: 
$ goal clerk rawsend -f signout.tx -d ~/node/testnet

If you didn't get rejection, the grouped transaction is commited and amount is cut from host account sent to escrow account as well as transaction fees (paid by sender)
