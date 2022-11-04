#!/usr/bin/env python3

""" Example of a Pay-to-Witness-Script-Hash transaction.
"""

import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
sys.path.append(os.path.dirname(SCRIPT_DIR + "../lib."))

from lib.encoder import encode_tx, encode_script
from lib.hash    import hash160, hash256, sha256
from lib.helper  import decode_address
from lib.sign    import sign_tx
from lib.rpc     import RpcSocket
from lib.helper  import get_utxos, get_fee, get_amount

# Init wallet:
wallet = input("Enter wallet name: ")
rpc = RpcSocket({ 'wallet': wallet })
assert rpc.check()

# Get amount
amount = get_amount()

# Get fee
fee = get_fee()

# Get utxos for input to meet amount
utxos = get_utxos(rpc, amount + fee)

## Get a change address for sender
change_txout = rpc.get_recv(fmt='base58')
change_pubkey_hash  = decode_address(change_txout['address'])

# Set the amount to send and change value
utxos_sum = sum(u['value'] for u in utxos)
change_value = utxos_sum - amount - fee

## We will also grab a new receiving address,
## and lock the funds to this address.
recv = rpc.get_recv()

## Replace this default preimage with your own secret.
secret_preimage = input("Enter your secret: ")

## Convert the secret to bytes, then hash using hash160 function.
secret_bytes = secret_preimage.encode('utf8').hex()
secret_hash  = hash160(secret_bytes).hex()

## This is where we specify the version number for the program interpreter. 
## We'll be using version 0.
script_version = 0

## Here is the locking script that we will be using. We are going to
## require the redeemer to reveral the secret, along with their public
## key for the receipt address, and matching signature.
script_words = [
    'OP_HASH160', secret_hash, 'OP_EQUALVERIFY', 
    'OP_DUP', 'OP_HASH160', hash160(recv['pub_key']).hex(), 'OP_EQUALVERIFY', 
    'OP_CHECKSIG'
]

## This is the hex-encoded format of the script. We will present this when 
## we unlock and spend the output. It should match the pre-image used for 
## making the script hash.
redeem_script = encode_script(script_words, prepend_len=False).hex()

## We hash the script using sha256, then provide a version number
## along with the hash. This will lock the transaction output to 
## accept only the program script which matches the hash.
script_hash = sha256(redeem_script).hex()


# Add all utxos as vin:
all_vins = []
for u in utxos:
    vin = {}
    vin['txid'] = u['txid']
    vin['vout'] = u['vout']
    vin['script_sig'] = []
    vin['sequence'] = 0xFFFFFFFF
    all_vins.append(vin)

## The initial locking transaction. This spends the utxo from our funding 
## transaction, and moves the funds to the utxo for our witness program.
locking_tx = {
    'version': 1,
    'vin': all_vins,
    'vout': [
        {
            'value': amount,
            'script_pubkey': [ script_version, script_hash ]
        },
        {
            'value': change_value,
            'script_pubkey': ['OP_DUP', 'OP_HASH160', change_pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
        }
    ],
    'locktime': 0
}

## Encode the transaction into raw hex,
## and calculate the transaction ID
locking_hex  = encode_tx(locking_tx)
locking_txid = hash256(bytes.fromhex(locking_hex))[::-1].hex()

## Sign the transaction using our key-pair from the utxo.
# Sign all inputs:
for index, utxo in enumerate(utxos):
    ## The redeem script is a basic Pay-to-Pubkey-Hash template.
    signature = sign_tx(
        locking_tx, 
        index,
        utxo['value'], 
        utxo['pubkey_hash'], 
        utxo['priv_key']
    )

    ## Add the signature and public key to the transaction.
    locking_tx['vin'][index]['witness'] = [ signature, utxo['pub_key'] ]

print(f'''
# Pay-to-Witness-Script-Hash Example

Locking Txid:
{locking_txid}

Redeem Script:
{redeem_script}

Locking Tx:
{encode_tx(locking_tx)}
''')

print("Sending transaction via RPC")
rpc.send_transaction(locking_tx)

## Bech32 addresses will decode into a script version and pubkey hash.
script_version, pubkey_hash = decode_address(recv['address'])

## This transaction will redeem the previous utxo by providing the secret 
## pre-image, plus the public key and signature, plus the witness program. 
## Once the transaction is confirmed, your wallet software should recognize 
## this utxo as spendable.
redeem_tx = {
    'version': 1,
    'vin': [{
        'txid': locking_txid,
        'vout': 0,
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': amount - 500,
        'script_pubkey': [ script_version, pubkey_hash ]
    }],
    'locktime':0
}

redeem_sig = sign_tx(
  redeem_tx,
  0,
  amount,
  redeem_script,
  recv['priv_key']
)

redeem_tx['vin'][0]['witness'] = [ redeem_sig, recv['pub_key'], secret_bytes, redeem_script ]

print(f'Unlocking Tx:\n{encode_tx(redeem_tx)}')

print("Sending transaction via RPC")
rpc.send_transaction(redeem_tx)