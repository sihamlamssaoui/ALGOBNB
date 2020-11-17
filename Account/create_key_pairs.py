# Copyright Cristian Lepore

# This file creates the private and public key

from algosdk import account, mnemonic

# This function will generate a public/private key pair¶
def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

# This is the Main function
def main():
    generate_algorand_keypair()

# Start of the program
if __name__ == "__main__":
    main()