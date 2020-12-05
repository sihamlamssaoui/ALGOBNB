# Copyright Cristian Lepore

# Create an account

# Import the modules
from algosdk import account, mnemonic

# Generate a public/private keypair with the generate_account function.
private_key, public_address = account.generate_account()

# Print the private key an Algorand address so you can see what they look like.
print("Base64 Private Key: {}\nPublic Algorand Address: {}\n".format(private_key, public_address))

# Retrieve from private key
print(mnemonic.from_private_key(private_key))
