#!/usr/bin/env python3

"""
Example of a Pay-to-Witness-Pubkey-Hash (P2WPKH) transaction.
"""

import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
sys.path.append(os.path.dirname(SCRIPT_DIR + "../lib."))

from lib.encoder import encode_tx, encode_script
from lib.hash    import hash256
from lib.helper  import decode_address, hash_script, get_txid
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

## Get a change address - using segwit address.
change_txout     = rpc.get_recv()
_, change_redeem_script = decode_address(change_txout['address'])

# Get payment address
receiver_type = None
receiver_address = None
while receiver_type != "a" and receiver_type != "w":
    receiver_type = input("Select one of the following options:\n(a) Enter recipient address\n(w) Enter recipient wallet name in bitcoin core:\n")
if receiver_type == "a":
    rec_address = input("Enter recipient payment segwit address: ")
    if not rec_address.startswith('tb') and not rec_address.startswith('bc'):
        raise Exception("Only segwit addresses supported")
    receiver_address = {'address': rec_address}
elif receiver_type == "w":
    receiver_wallet = input("Enter recipient wallet name: ")
    receiver_rpc = RpcSocket({ 'wallet': receiver_wallet })
    assert receiver_rpc.check()
    receiver_address = receiver_rpc.get_recv()

_, receiver_redeem_script = decode_address(receiver_address['address'])

# Set the amount to send and change value
utxos_sum = sum(u['value'] for u in utxos)
change_value = utxos_sum - amount - fee

## The initial spending transaction. This tx spends a previous utxo,
## and commits the funds to our P2WPKH transaction.

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
            'script_pubkey': [0, receiver_redeem_script]
        },
        {
            'value': change_value,
            'script_pubkey': [0, change_redeem_script]
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
        tx,                # The transaction.
        index,                      # The input being signed.
        utxo['value'],    # The value of the utxo being spent.
        redeem_script,          # The redeem script to unlock the utxo. 
        utxo['priv_key']  # The private key to the utxo pubkey hash.
    )

    ## Include the arguments needed to unlock the redeem script.
    tx['vin'][index]['witness'] = [ signature, utxo['pub_key'] ]

print(f'''
## Pay-to-Witness-Pubkey-Hash Example ##

-- Transaction Id --
{txid}

-- Transaction Hex --
{encode_tx(tx)}
''')

#print("Would send transaction here")
rpc.send_transaction(tx)