# dAirBnB

## Test

goal asset create --creator YCVEJYJ2BM3XN7IXSQ4Z44TR4V6KNO5DEJ3Z7SP5FW3EXKLPKKPWH4FXSY --decimals 0 --name "Reputation"  --total 1 --unitname REP --asseturl "\Documents\Reputation_asset.txt" -d data/

goal asset send -a 0 --assetid 13258381 -f 76RB4ZRMJOQRBQ3FO5MLBWUSDYNXF7MIC4F5ORUFRVA625XWZOVRIFJCSE -t 76RB4ZRMJOQRBQ3FO5MLBWUSDYNXF7MIC4F5ORUFRVA625XWZOVRIFJCSE --creator YCVEJYJ2BM3XN7IXSQ4Z44TR4V6KNO5DEJ3Z7SP5FW3EXKLPKKPWH4FXSY -d data/

goal asset freeze --freezer YCVEJYJ2BM3XN7IXSQ4Z44TR4V6KNO5DEJ3Z7SP5FW3EXKLPKKPWH4FXSY --freeze=false --account 76RB4ZRMJOQRBQ3FO5MLBWUSDYNXF7MIC4F5ORUFRVA625XWZOVRIFJCSE --creator YCVEJYJ2BM3XN7IXSQ4Z44TR4V6KNO5DEJ3Z7SP5FW3EXKLPKKPWH4FXSY --assetid 13258381 --out=unsignedtransaction1.tx -d data/

goal asset send -a 1 --assetid 13258381 -f YCVEJYJ2BM3XN7IXSQ4Z44TR4V6KNO5DEJ3Z7SP5FW3EXKLPKKPWH4FXSY -t 76RB4ZRMJOQRBQ3FO5MLBWUSDYNXF7MIC4F5ORUFRVA625XWZOVRIFJCSE --creator YCVEJYJ2BM3XN7IXSQ4Z44TR4V6KNO5DEJ3Z7SP5FW3EXKLPKKPWH4FXSY --out=unsignedtransaction2.tx -d data/

goal asset freeze --freezer YCVEJYJ2BM3XN7IXSQ4Z44TR4V6KNO5DEJ3Z7SP5FW3EXKLPKKPWH4FXSY --freeze=true --account 76RB4ZRMJOQRBQ3FO5MLBWUSDYNXF7MIC4F5ORUFRVA625XWZOVRIFJCSE --creator YCVEJYJ2BM3XN7IXSQ4Z44TR4V6KNO5DEJ3Z7SP5FW3EXKLPKKPWH4FXSY --assetid 13258381 --out=unsignedtransaction3.tx -d data/

cat unsignedtransaction1.tx unsignedtransaction2.tx unsignedtransaction3.tx > combinedtransactions.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx -d data/

goal clerk sign -i groupedtransactions.tx -o signout.tx -d data/

goal clerk rawsend -f signout.tx -d data/

---

#### Copyright &copy; 2020 dAirbnb
