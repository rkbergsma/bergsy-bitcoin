#!/usr/bin/env python3

""" Example of a Pay-to-Witness-Script-Hash transaction.
"""

import os, sys

# sys.path.append(os.path.dirname(__file__).split('/transactions')[0])
sys.path.insert(1, os.path.abspath(".."))

from lib.encoder import encode_tx, encode_script
from lib.hash    import hash160, hash256, sha256
from lib.helper  import decode_address
from lib.sign    import sign_tx
from lib.rpc     import RpcSocket

## Setup our RPC sockets.
party1_rpc = RpcSocket({ 'wallet': 'bergs-wallet' })
assert party1_rpc.check()
party2_rpc = RpcSocket({ 'wallet': 'bob_wallet' })
assert party2_rpc.check()
party3_rpc = RpcSocket({ 'wallet': 'Legacy' })
assert party3_rpc.check()

## First, we will lookup an existing utxo,
## and use that to fund our transaction.
utxo = party1_rpc.get_utxo(0)

## We will also grab a new receiving address,
## and lock the funds to this address.
## Bob is our recipient.
party1_recv = party1_rpc.get_recv()
party2_recv = party2_rpc.get_recv()
party3_recv = party3_rpc.get_recv()

## This is where we specify the version number for the program interpreter. 
## We'll be using version 0.
script_version = 0

## Here is the locking script that we will be using. We are going to
## require the redeemer to reveral the secret, along with their public
## key for the receipt address, and matching signature.
script_words = [
    'OP_2',
    party1_recv['pub_key'],
    party2_recv['pub_key'],
    party3_recv['pub_key'],
    'OP_3',
    'OP_CHECKMULTISIG'
  ]

## This is the hex-encoded format of the script. We will present this when 
## we unlock and spend the output. It should match the pre-image used for 
## making the script hash.
redeem_script = encode_script(script_words, prepend_len=False).hex()

## We hash the script using sha256, then provide a version number
## along with the hash. This will lock the transaction output to 
## accept only the program script which matches the hash.
script_hash = sha256(redeem_script).hex()

## Calculate the value of the transaction output, minus fees.
locking_tx_value = utxo['value'] - 1000

## The initial locking transaction. This spends the utxo from our funding 
## transaction, and moves the funds to the utxo for our witness program.
locking_tx = {
    'version': 1,
    'vin': [{
        'txid': utxo['txid'],
        'vout': utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': locking_tx_value,
        'script_pubkey': [ script_version, script_hash ]
    }],
    'locktime': 0
}

## Encode the transaction into raw hex,
## and calculate the transaction ID
locking_hex  = encode_tx(locking_tx)
locking_txid = hash256(bytes.fromhex(locking_hex))[::-1].hex()

## Sign the transaction using our key-pair from the utxo.
locking_sig = sign_tx(
  locking_tx, 
  0,
  utxo['value'], 
  utxo['pubkey_hash'], 
  utxo['priv_key']
)

## Add the signature and public key to the transaction.
locking_tx['vin'][0]['witness'] = [ locking_sig, utxo['pub_key'] ]

print(f'''
# Pay-to-Witness-Script-Hash Multisig Example

Locking Txid:
{locking_txid}

Redeem Script:
{redeem_script}

Locking Tx:
{encode_tx(locking_tx)}
''')

## Bech32 addresses will decode into a script version and pubkey hash.
script_version, pubkey_hash = decode_address(party2_recv['address'])

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
        'value': locking_tx_value - 1000,
        'script_pubkey': [ script_version, pubkey_hash ]
    }],
    'locktime':0
}

redeem_sig_1 = sign_tx(
  redeem_tx,
  0,
  locking_tx_value,
  redeem_script,
  party1_recv['priv_key']
)

redeem_sig_2 = sign_tx(
  redeem_tx,
  0,
  locking_tx_value,
  redeem_script,
  party2_recv['priv_key']
)

redeem_sig_3 = sign_tx(
  redeem_tx,
  0,
  locking_tx_value,
  redeem_script,
  party3_recv['priv_key']
)

redeem_tx['vin'][0]['witness'] = [ 0, redeem_sig_1, redeem_sig_2, redeem_sig_3, redeem_script ]

print(f'Unlocking Tx:\n{encode_tx(redeem_tx)}')