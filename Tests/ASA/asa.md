# dAirBnB

## create asset using goal:

<<<<<<< HEAD
Create ASA:\
=======
Create ASA\
>>>>>>> 48939d92e4ebc0ef8c72b5b7ffe19a43e01ab936
goal asset create --creator A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I --decimals 0 --name "Reputation"  --total 1 --unitname REP --asseturl "\Documents\Reputation_asset.txt" -d ~/node/testnet

---

unfreeze:\
goal asset freeze --freezer A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I  --freeze=false --account A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I --creator A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I --asset REP --out=unsignedtransaction1.tx -d ~/node/testnet

---

Optin:\
goal asset send -a 0 --assetid 13205902 -f 7BHXE46DOOVFEMIHB7KSWJUY4UWTRVE4L5WIVXLHVXQWOCBPRA7EWFLPKU  -t 7BHXE46DOOVFEMIHB7KSWJUY4UWTRVE4L5WIVXLHVXQWOCBPRA7EWFLPKU  --creator A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I --out=unsignedtransaction2.tx -d ~/node/testnet

---

call to stateful contract:\
goal app call --app-id app_ID --app-arg "str:asa_allowed_address" --from=7BHXE46DOOVFEMIHB7KSWJUY4UWTRVE4L5WIVXLHVXQWOCBPRA7EWFLPKU --out=unsignedtransaction3.tx -d ~/node/testnet

---

Transfer:\
goal asset send -a 1 --assetid 13205902 -f A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I  -t 7BHXE46DOOVFEMIHB7KSWJUY4UWTRVE4L5WIVXLHVXQWOCBPRA7EWFLPKU --creator A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I --out=unsignedtransaction4.tx  -d ~/node/testnet

---

Freeze:\
goal asset freeze --freezer A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I  --freeze=true --account A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I --creator A62HUFIM4MLPWN6USRM2FJBHQG6CN3NKQ4T2MOKAO3TL47NDWVKYY3KV2I --asset REP --out=unsignedtransaction5.tx -d ~/node/testnet

---

Combine Tx:\
cat unsignedtransaction1.tx unsignedtransaction2.tx unsignedtransaction3.tx unsignedtransaction4.tx unsignedtransaction5.tx> combinedtransactions.tx

---

Group Tx:\
goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

---

Sign Tx group:\
goal clerk sign -i groupedtransactions.tx -o signout.tx -d ~/node/testnet

---

Execute Tx grp:\
goal clerk rawsend -f signout.tx -d ~/node/testnet

---

#### Copyright &copy; 2020 dAirbnb