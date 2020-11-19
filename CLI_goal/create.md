# ALGOBNB

## Create asset

We have the following account: PWBN75WEWPJE2FSNI6Q43RQQTP3U5AY2NRCO5MUA6HPOZLHYYUHLRRE26I

Create a Reputation asset
./goal asset create --asseturl "\Documents\Reputation_asset.txt" --creator PWBN75WEWPJE2FSNI6Q43RQQTP3U5AY2NRCO5MUA6HPOZLHYYUHLRRE26I --decimals 0 --name "Reputation" --note "Reputation token" --total 1 --unitname REP --datadir data/ --wallet myWallet

## Manage asset

We have created a second account BCQO4VC3HEFLRSSLQZGV4AZLWJZI6UCFSVB2GT6XVOJRY43EHVUNN6M5XY that manages the asset
./goal asset config --assetid 13171801 --creator PWBN75WEWPJE2FSNI6Q43RQQTP3U5AY2NRCO5MUA6HPOZLHYYUHLRRE26I --manager BCQO4VC3HEFLRSSLQZGV4AZLWJZI6UCFSVB2GT6XVOJRY43EHVUNN6M5XY --new-clawback "" --new-freezer "" --note "Reputation token" --datadir data/ --wallet myWallet