#!/usr/bin/env python3

"""
Example of a Pay-to-Pubkey-Hash (P2PKH) transaction.

P2PKH is the most common type of transaction that is used 
on the Bitcoin payment network.

We will construct a transaction that is locked to the hash
of a public key. In order to unlock the tranasction, a user
will have to provide the un-hashed public key, along with a
digital signature which shares that same public key.

You can generate a block in order to commit this transaction 
to the blockchain (if you are using regtest).
"""

import os, sys

# sys.path.append(os.path.dirname(__file__).split('/transactions')[0])
sys.path.insert(1, os.path.abspath(".."))

from lib.encoder import encode_tx
from lib.helper  import decode_address
from lib.hash    import hash256
from lib.sign    import sign_tx
from lib.rpc     import RpcSocket

def get_utxos(rpc, amt):
    utxos = []
    tx_in_sum = 0
    i = 0
    while tx_in_sum < amt:
        utxo = rpc.get_utxo(i)
        utxos.append(utxo)
        tx_in_sum = tx_in_sum + utxo['value']
        i = i + 1
    return utxos

# Init wallet:
testnet_wallet = input("Enter testnet wallet:")
rpc = RpcSocket({ 'wallet': testnet_wallet })
assert rpc.check()

# Get amount
amount = input("Enter amount to send:")

# Get utxos for input to meet amount
utxos = get_utxos(rpc, amount)

## Get a change address for sender
change_txout = rpc.get_recv(fmt='base58')
pubkey_hash  = decode_address(change_txout['address'])

# Get payment address
receiver_address = input("Enter payment address:")
receiver_pubkey_hash = decode_address(receiver_address['address'])





# ## Setup our RPC socket.
# bob_rpc = RpcSocket({ 'wallet': 'bob_wallet' })
# assert bob_rpc.check()

## Get a utxo for Alice.
alice_utxo = rpc.get_utxo(0)

## Get a change address for Alice.
alice_change_txout = rpc.get_recv(fmt='base58')
alice_pubkey_hash  = decode_address(alice_change_txout['address'])

## Get a payment address for Bob.
bob_payment_txout = bob_rpc.get_recv(fmt='base58')
bob_pubkey_hash   = decode_address(bob_payment_txout['address'])

## Calculate our output amounts.
fee = 1000
bob_recv_value = alice_utxo['value'] // 2
alice_change_value = alice_utxo['value'] // 2 - fee

## The spending transaction.
atob_tx = {
    'version': 1,
    'vin': [{
        # We are unlocking the utxo from Alice.
        'txid': alice_utxo['txid'],
        'vout': alice_utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [
        {
            'value': bob_recv_value,
            'script_pubkey': ['OP_DUP', 'OP_HASH160', bob_pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
        },
        {
            'value': alice_change_value,
            'script_pubkey': ['OP_DUP', 'OP_HASH160', alice_pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
        }
    ],
    'locktime': 0
}

## Serialize the transaction and calculate the TXID.
atob_hex  = encode_tx(atob_tx)
atob_txid = hash256(bytes.fromhex(atob_hex))[::-1].hex()

## The redeem script is a basic Pay-to-Pubkey-Hash template.
redeem_script = f"76a914{alice_utxo['pubkey_hash']}88ac"

## We are signing Alice's UTXO using BIP143 standard.
alice_signature = sign_tx(
    atob_tx,                # The transaction.
    0,                      # The input being signed.
    alice_utxo['value'],    # The value of the utxo being spent.
    redeem_script,          # The redeem script to unlock the utxo. 
    alice_utxo['priv_key']  # The private key to the utxo pubkey hash.
)

## Include the arguments needed to unlock the redeem script.
atob_tx['vin'][0]['witness'] = [ alice_signature, alice_utxo['pub_key'] ]

print(f'''
## Pay-to-Pubkey-Hash Example ##

-- Transaction Id --
{atob_txid}

-- Alice UTXO --
     Txid : {alice_utxo['txid']}
     Vout : {alice_utxo['vout']}
    Value : {alice_utxo['value']}
     Hash : {alice_utxo['pubkey_hash']}

-- Sending to Bob --
  Address : {bob_payment_txout['address']}
    Coins : {bob_recv_value}

-- Change --
  Address : {alice_change_txout['address']}
      Fee : {fee}
    Coins : {alice_change_value}

-- Hex --
{encode_tx(atob_tx)}
''')

rpc.send_transaction(atob_tx)
