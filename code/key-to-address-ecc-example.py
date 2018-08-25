# - install pybitcointools from git:
#    - pip install git+https://github.com/robermann/pybitcointools
#     - (see https://github.com/vbuterin/pybitcointools/issues/153 for the reason of the fork; there are conflicts with "import bitcoin")
#   
#     my pip freeze:
#        bitcoin==1.1.42
#        pybitcointools==1.1.42     (installed as above)
#        python-bitcoinlib==0.10.1
#

from __future__ import print_function
import pybitcointools

# Generate a random private key
valid_private_key = False
while not valid_private_key:
    private_key = pybitcointools.random_key()
    decoded_private_key = pybitcointools.decode_privkey(private_key, 'hex')
    valid_private_key = 0 < decoded_private_key < pybitcointools.N

print("Private Key (hex) is: ", private_key)
print("Private Key (decimal) is: ", decoded_private_key)

# Convert private key to WIF format
wif_encoded_private_key = pybitcointools.encode_privkey(decoded_private_key, 'wif')
print("Private Key (WIF) is: ", wif_encoded_private_key)

# Add suffix "01" to indicate a compressed private key
compressed_private_key = private_key + '01'
print("Private Key Compressed (hex) is: ", compressed_private_key)

# Generate a WIF format from the compressed private key (WIF-compressed)
wif_compressed_private_key = pybitcointools.encode_privkey(
    pybitcointools.decode_privkey(compressed_private_key, 'hex'), 'wif_compressed')
print("Private Key (WIF-Compressed) is: ", wif_compressed_private_key)

# Multiply the EC generator point G with the private key to get a public key point
public_key = pybitcointools.fast_multiply(pybitcointools.G, decoded_private_key)
print("Public Key (x,y) coordinates is:", public_key)

# Encode as hex, prefix 04
hex_encoded_public_key = pybitcointools.encode_pubkey(public_key, 'hex')
print("Public Key (hex) is:", hex_encoded_public_key)

# Compress public key, adjust prefix depending on whether y is even or odd
(public_key_x, public_key_y) = public_key
compressed_prefix = '02' if (public_key_y % 2) == 0 else '03'
hex_compressed_public_key = compressed_prefix + (pybitcointools.encode(public_key_x, 16).zfill(64))
print("Compressed Public Key (hex) is:", hex_compressed_public_key)

# Generate pybitcointools address from public key
print("pybitcointools Address (b58check) is:", pybitcointools.pubkey_to_address(public_key))

# Generate compressed pybitcointools address from compressed public key
print("Compressed pybitcointools Address (b58check) is:",
      pybitcointools.pubkey_to_address(hex_compressed_public_key))
