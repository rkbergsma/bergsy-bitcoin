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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
sys.path.append(os.path.dirname(SCRIPT_DIR + "../lib."))
#sys.path.append(os.path.dirname(__file__).split('/transactions')[0])
#sys.path.insert(1, os.path.abspath(".."))

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

def get_fee():
    fee = input("Enter fee in satoshis (or press enter for default 1000): ")
    try:
        fee = int(fee)
    except ValueError:
        fee = 1000
        print("Using default fee of 1000")
    return fee

def get_amount():
    amount = input("Enter amount to send (in satoshis): ")
    try:
        amount = int(amount)
    except ValueError:
        print("Invalid amount, must be an integer")
        raise
    return amount

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
pubkey_hash  = decode_address(change_txout['address'])

# Get payment address
receiver_type = None
receiver_address = None
while receiver_type != "a" and receiver_type != "w":
    receiver_type = input("Select one of the following options:\n(a) Enter recipient address\n(w) Enter recipient wallet name in bitcoin core:\n")
if receiver_type == "a":
    receiver_address = input("Enter recipient payment address: ")
elif receiver_type == "w":
    receiver_wallet = input("Enter recipient wallet name: ")
    receiver_rpc = RpcSocket({ 'wallet': receiver_wallet })
    assert receiver_rpc.check()
    receiver_address = receiver_rpc.get_recv(fmt='base58')

receiver_pubkey_hash = decode_address(receiver_address['address'])

# Set the amount to send and change value
utxos_sum = sum(u['value'] for u in utxos)
change_value = utxos_sum - amount - fee

# Add all utxos as vin:
all_vins = []
for u in utxos:
    vin = {}
    vin['txid'] = u['txid']
    vin['vout'] = u['vout']
    vin['script_sig'] = []
    vin['sequence'] = 0xFFFFFFFF
    all_vins.append(vin)

## The spending transaction.
tx = {
    'version': 1,
    'vin': all_vins,
    'vout': [
        {
            'value': amount,
            'script_pubkey': ['OP_DUP', 'OP_HASH160', receiver_pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
        },
        {
            'value': change_value,
            'script_pubkey': ['OP_DUP', 'OP_HASH160', pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
        }
    ],
    'locktime': 0
}

## Serialize the transaction and calculate the TXID.
tx_hex  = encode_tx(tx)
txid = hash256(bytes.fromhex(tx_hex))[::-1].hex()

# Sign all inputs:
for index, utxo in enumerate(utxos):
    ## The redeem script is a basic Pay-to-Pubkey-Hash template.
    redeem_script = f"76a914{utxo['pubkey_hash']}88ac"

    ## We are signing Alice's UTXO using BIP143 standard.
    signature = sign_tx(
        tx,                     # The transaction.
        index,                  # The input being signed.
        utxo['value'],    # The value of the utxo being spent.
        redeem_script,          # The redeem script to unlock the utxo. 
        utxo['priv_key']  # The private key to the utxo pubkey hash.
    )

    ## Include the arguments needed to unlock the redeem script.
    tx['vin'][index]['witness'] = [ signature, utxo['pub_key'] ]

print(f'''
## Pay-to-Pubkey-Hash Example ##

-- Transaction Id --
{txid}

-- Transaction Hex --
{encode_tx(tx)}
''')

print("Would send transaction here")
#rpc.send_transaction(tx)
