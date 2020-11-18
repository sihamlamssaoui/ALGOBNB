// Copyright Cristian Lepore

// Create a Wallet and generate an account within the wallet.

const algosdk = require('algosdk');

const kmdtoken = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const kmdserver = "localhost";
const kmdport = "4002";

const kmdclient = new algosdk.Kmd(kmdtoken, kmdserver, kmdport);

var walletid = null;
var wallethandle = null;

(async() => {
    let walletid = (await kmdclient.createWallet("myWallet", "mypassword", "", "sqlite")).wallet.id;
    console.log("Created wallet:", walletid);

    let wallethandle = (await kmdclient.initWalletHandle(walletid, "mypassword")).wallet_handle_token;
    console.log("Got wallet handle:", wallethandle);

    let address1 = (await kmdclient.generateKey(wallethandle)).address;
    console.log("Created new account:", address1);
})().catch(e => {
    console.log(e);
});