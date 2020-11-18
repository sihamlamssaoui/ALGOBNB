# Copyright Cristian Lepore

# Retrieve keys

from algosdk import mnemonic

# This is a secret key used as example. Please, insert your sk.
private_key = 'KKqRIq3e+hYE0ifeA57XLu1hfrarO3lVbVaDl4YgJRTGbrFZLPgC/dw7rWTihwgGYwppUTmAygNXPLjy6VDMFA=='

# Retrieve the key
mnemonic_key = mnemonic.from_private_key (private_key)

# Print key
print("This is my key", mnemonic_key)
