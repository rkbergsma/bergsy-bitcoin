#!/usr/bin/env python3

"""
Example of a Pay-to-Witness-Pubkey-Hash (P2WPKH) transaction.
"""

import os, sys
import argparse
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
sys.path.append(os.path.dirname(SCRIPT_DIR + "../lib."))

from lib.encoder import encode_tx, encode_script
from lib.hash    import hash256, sha256
from lib.helper  import decode_address, hash_script, get_txid
from lib.sign    import sign_tx
from lib.rpc     import RpcSocket
from lib.helper  import get_utxos, get_fee, get_amount, get_change_address

def locking_tx_flow():
    rpc = get_wallet("Enter wallet name to fund multisig: ")
    amount = get_amount()
    fee = get_fee()
    utxos = get_utxos(rpc, amount + fee)
    change_address = get_change_address(rpc)
    redeem_script = generate_multisig_script(rpc)
    locking_tx = generate_locking_tx(amount, fee, utxos, change_address, redeem_script)
    tx_hex  = encode_tx(locking_tx)
    txid = hash256(bytes.fromhex(tx_hex))[::-1].hex()
    locking_tx = sign_all_inputs(locking_tx, utxos)
    print_locking_summary(locking_tx, txid)
    create_and_save_redeem_tx(txid, amount, redeem_script)

def get_wallet(message):
    wallet = input(message)
    rpc = RpcSocket({ 'wallet': wallet })
    assert rpc.check()
    return rpc

def generate_multisig_script(rpc):
    party1_recv = rpc.get_recv()
    #party2_recv = get_participant_address(rpc)
    #party3_recv = get_participant_address(rpc)
    party2_recv = input("Enter recipient pubkey: ")
    party3_recv = input("Enter recipient pubkey: ")
    script_words = [
        'OP_2',
        party1_recv['pub_key'],
        party2_recv,
        party3_recv,
        'OP_3',
        'OP_CHECKMULTISIG'
    ]
    redeem_script = encode_script(script_words, prepend_len=False).hex()
    print("Party 1 Address:", party1_recv['address'])
    #script_hash = sha256(redeem_script).hex()
    return redeem_script

def get_participant_address(rpc):
    address = input("Enter recipient payment segwit address: ")
    if not address.startswith('tb') and not address.startswith('bc'):
        raise Exception("Only segwit addresses supported")
    return rpc.get_address_info(address)

def generate_locking_tx(amount, fee, utxos, change_address, redeem_script):
    script_hash = sha256(redeem_script).hex()
    vins = generate_vins(utxos)

    utxos_sum = sum(u['value'] for u in utxos)
    change_value = utxos_sum - amount - fee

    locking_tx = {
        'version': 1,
        'vin': vins,
        'vout': [{
                'value': amount,
                'script_pubkey': [ 0, script_hash ]
            },
            {
                'value': change_value,
                'script_pubkey': [0, change_address]
            }
        ],
        'locktime': 0
    }
    return locking_tx

def generate_vins(utxos):
    all_vins = []
    for u in utxos:
        vin = {}
        vin['txid'] = u['txid']
        vin['vout'] = u['vout']
        vin['script_sig'] = []
        vin['sequence'] = 0xFFFFFFFF
        all_vins.append(vin)
    return all_vins

def sign_all_inputs(locking_tx, utxos):
    for index, utxo in enumerate(utxos):
        redeem_script = f"76a914{utxo['pubkey_hash']}88ac"
        signature = sign_tx(
            locking_tx,                # The transaction.
            index,                      # The input being signed.
            utxo['value'],    # The value of the utxo being spent.
            redeem_script,          # The redeem script to unlock the utxo. 
            utxo['priv_key']  # The private key to the utxo pubkey hash.
        )
        locking_tx['vin'][index]['witness'] = [ signature, utxo['pub_key'] ]
    return locking_tx

def print_locking_summary(locking_tx, txid):
    print(f'''
    ## Pay-to-Witness-Pubkey-Hash Example ##

    -- Transaction Id --
    {txid}

    -- Transaction Hex --
    {encode_tx(locking_tx)}
    ''')

def create_and_save_redeem_tx(txid, amount, redeem_script):
    print("Generating psbt redeem TX.")
    party1 = input("Enter party 1 address: ")
    party2 = input("Enter party 2 address: ")
    party3 = input("Enter party 3 address: ")

    script_version_1, pubkey_hash_1 = decode_address(party1)
    script_version_2, pubkey_hash_2 = decode_address(party2)
    script_version_3, pubkey_hash_3 = decode_address(party3)

    
    redeem_tx = {
        'version': 1,
        'vin': [{
            'txid': txid,
            'vout': 0,
            'script_sig': [],
            'sequence': 0xFFFFFFFF
        }],
        'vout': [
            {
                'value': amount // 3 - 1000, # sorry party1, you pay the fee
                'script_pubkey': [ script_version_1, pubkey_hash_1 ]
            },
            {
                'value': amount // 3 ,
                'script_pubkey': [ script_version_2, pubkey_hash_2 ]
            },
            {
                'value': amount // 3 ,
                'script_pubkey': [ script_version_3, pubkey_hash_3 ]
            }
        ],
        'locktime':0
    }
    psbt = {
        'redeem_script': redeem_script,
        'amount': amount,
        'redeem_tx': redeem_tx
    }
    write_json(psbt)

def write_json(input, filename = "psbt.json"):
    print("Writing file", filename)
    json_object = json.dumps(input)
    with open(filename, "w") as o:
        o.write(json_object)

def sign_tx_flow(psbt_file):
    psbt = read_psbt(psbt_file)

    rpc = get_wallet("Enter wallet name to connect for RPC: ")
    signer_address = input("Enter address you are signing for: ")
    signer_address = rpc.get_address_info(signer_address)
    signature = sign(psbt['redeem_tx'], psbt['amount'], psbt['redeem_script'], signer_address)
    
    signature_index = input("Please enter index of your signature: ")
    signature_index = int(signature_index)

    if 'signatures' not in psbt:
        psbt['signatures'] = {signature_index: signature}
    else:
        psbt['signatures'][signature_index] = signature
    write_json(psbt, "psbt_signed.json")

def read_psbt(psbt_input):
    print("Reading in psbt:", psbt_input)
    with open(psbt_input, 'r') as openfile:
        json_object = json.load(openfile)
        return json_object

# def sign_tx_flow_old():
#     rpc = get_wallet("Enter wallet name to connect for RPC: ")

#     locking_txid = input("Please enter locking txid: ")

#     party1, party2, party3 = get_addresses(rpc)

#     locking_tx = rpc.get_transaction(locking_txid)
#     locking_tx_value = int(-100000000 * locking_tx['amount'])

#     script_version_1, pubkey_hash_1 = decode_address(party1['address'])
#     script_version_2, pubkey_hash_2 = decode_address(party2['address'])
#     script_version_3, pubkey_hash_3 = decode_address(party3['address'])
    
#     redeem_tx = {
#         'version': 1,
#         'vin': [{
#             'txid': locking_txid,
#             'vout': 0,
#             'script_sig': [],
#             'sequence': 0xFFFFFFFF
#         }],
#         'vout': [
#             {
#                 'value': locking_tx_value // 3 - 1000, # sorry party1, you pay the fee
#                 'script_pubkey': [ script_version_1, pubkey_hash_1 ]
#             },
#             {
#                 'value': locking_tx_value // 3 ,
#                 'script_pubkey': [ script_version_2, pubkey_hash_2 ]
#             },
#             {
#                 'value': locking_tx_value // 3 ,
#                 'script_pubkey': [ script_version_3, pubkey_hash_3 ]
#             }
#         ],
#         'locktime':0
#     }

#     redeem_script = input("Please enter redeem script: ")
#     if 'priv_key' in party1:
#         sign(redeem_tx, locking_tx_value, redeem_script, party1)
#     elif 'priv_key' in party2:
#         sign(redeem_tx, locking_tx_value, redeem_script, party2)
#     elif 'priv_key' in party3:
#         sign(redeem_tx, locking_tx_value, redeem_script, party3)

def sign(redeem_tx, locking_tx_value, redeem_script, party):
    signature = sign_tx(
        redeem_tx,
        0,
        locking_tx_value,
        redeem_script,
        party['priv_key']
    )
    return signature

def get_addresses(rpc):
    party1_address = input("Enter party 1's address: ")
    party1_address = rpc.get_address_info(party1_address)
    
    party2_address = input("Enter party 2's address: ")
    party2_address = rpc.get_address_info(party2_address)
    
    party3_address = input("Enter party 3's address: ")
    party3_address = rpc.get_address_info(party3_address)

    return party1_address, party2_address, party3_address


def redeem_tx_flow(psbt_file):
    rpc = get_wallet("Enter wallet name to connect for RPC: ")
    psbt = read_psbt(psbt_file)
    if 'signatures' in psbt and len(psbt['signatures']) >= 2:
        signatures = [v for k,v in sorted(psbt['signatures'].items())]
        psbt['redeem_tx']['vin'][0]['witness'] = [ 0, signatures[0], signatures[1], psbt['redeem_script'] ]
        final_redeem_tx = psbt['redeem_tx']
        print(f'\nFinal Valid Unlocking Tx:\n{encode_tx(final_redeem_tx)}')
        print("Would use rpc to send transaction here")
    else:
        raise Exception("Either signatures are not present or there are not enough signatures")


# def redeem_tx_flow_old():
#     rpc = get_wallet("Enter wallet name to connect for RPC: ")

#     locking_txid = input("Please enter locking txid: ")

#     party1, party2, party3 = get_addresses(rpc)

#     locking_tx = rpc.get_transaction(locking_txid)

#     script_version_1, pubkey_hash_1 = decode_address(party1['address'])
#     script_version_2, pubkey_hash_2 = decode_address(party2['address'])
#     script_version_3, pubkey_hash_3 = decode_address(party3['address'])
    
#     redeem_tx = {
#         'version': 1,
#         'vin': [{
#             'txid': locking_txid,
#             'vout': 0,
#             'script_sig': [],
#             'sequence': 0xFFFFFFFF
#         }],
#         'vout': [
#             {
#                 'value': locking_tx['amount'] // 3 - 1000, # sorry party1, you pay the fee
#                 'script_pubkey': [ script_version_1, pubkey_hash_1 ]
#             },
#             {
#                 'value': locking_tx['amount'] // 3 ,
#                 'script_pubkey': [ script_version_2, pubkey_hash_2 ]
#             },
#             {
#                 'value': locking_tx['amount'] // 3 ,
#                 'script_pubkey': [ script_version_3, pubkey_hash_3 ]
#             }
#         ],
#         'locktime':0
#     }

#     redeem_script = input("Please enter redeem script: ")
#     signature_1 = input("Please enter signature 1: ")
#     signature_2 = input("Please enter signature 2: ")
#     redeem_tx['vin'][0]['witness'] = [ 0, signature_1, signature_2, redeem_script ]
#     print(f'\nFinal Valid Unlocking Tx:\n{encode_tx(redeem_tx)}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Bitcoin python multisig')
    parser.add_argument('-l', '--locking', action='store_true', default=False)
    parser.add_argument('-s', '--sign', action='store_true', default=False)
    parser.add_argument('-p', '--psbt', action='store', default=None)
    parser.add_argument('-r', '--redeem', action='store_true', default=False)
    args = parser.parse_args()
    if args.locking:
        locking_tx_flow()
    elif args.sign:
        if not args.psbt:
            raise Exception("Please input psbt to sign via -p or --psbt arg")
        sign_tx_flow(args.psbt)
    elif args.redeem:
        if not args.psbt:
            raise Exception("Please input psbt to sign via -p or --psbt arg")
        redeem_tx_flow(args.psbt)
    else:
        print("Please input either -l to generate a locking multisig or -s to sign a multisig")
