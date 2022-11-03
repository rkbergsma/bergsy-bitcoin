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
from copy import deepcopy

def get_party_wallet(greeting):
  wallet_name = input(greeting)
  try:
    rpc = RpcSocket({ 'wallet': wallet_name })
    assert rpc.check()
    return rpc
  except Exception as e:
    print("Uh oh, either that wallet doesn't exist or there was an issue initializing it.")
    print("Error text:", str(e))
    print("Please try again!")
    return get_party_wallet(greeting)

def get_utxo():
  party_to_fund = get_party_to_fund()
  try:
    if party_to_fund == 1:
      return party1_rpc.get_utxo(0)
    elif party_to_fund == 2:
      return party2_rpc.get_utxo(0)
    elif party_to_fund == 3:
      return party3_rpc.get_utxo(0)
    else:
      print("Not a valid party to fund!")
      return get_utxo()
  except Exception as e:
    print("Uh oh, that party doesn't have any UTXO!")
    print("Error text:", str(e))
    print("Please try again!")
    return get_utxo()

def get_party_to_fund():
  try:
    party_to_fund = input("\nWhich party will fund the multisig? (1, 2, or 3)\n")
    party_to_fund = int(party_to_fund)
    if party_to_fund not in [1, 2, 3]:
      print("Invalid party to fund, please enter either 1, 2, or 3:")
      return get_party_to_fund()
    else:
      return party_to_fund
  except ValueError as e:
    print("Please enter either 1, 2, or 3 for the party to fund the transaction.")
    return get_party_to_fund()

## Setup our RPC sockets.
print("Let's generate a 2-of-3 multisig transaction!")
print("For this exercise you need 3 wallets on the regtest network, each with some utxo that is spendable.")
party1_rpc = get_party_wallet("\nEnter the name of the regtest wallet for party 1:\n")
party2_rpc = get_party_wallet("\nEnter the name of the regtest wallet for party 2:\n")
party3_rpc = get_party_wallet("\nEnter the name of the regtest wallet for party 3:\n")

# Get utxo to fund the multisig
utxo = get_utxo()

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

print("DEBUG")
print(party3_recv)
print(utxo)

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

print("Going to send the funding transaction now!")
party1_rpc.send_transaction(locking_tx)

## Bech32 addresses will decode into a script version and pubkey hash.
recipient = 0
while recipient not in [1, 2, 3]:
  recipient = input("\nWho is the recipient of the funds? For simplicity, enter 1, 2, or 3 for party 1, 2, or 3:\n")
  try:
    recipient = int(recipient)
  except ValueError:
    print("Please enter 1, 2, or 3 for which party will receive the funds:")
    recipient = 0

if recipient == 1:
  script_version, pubkey_hash = decode_address(party1_recv['address'])
elif recipient == 2:
  script_version, pubkey_hash = decode_address(party2_recv['address'])
elif recipient == 3:
  script_version, pubkey_hash = decode_address(party3_recv['address'])
else:
  raise Exception("Got a bad recipient!") # should not happen due to check above

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

print("\nNow we need to sign the multisig transaction to spend it!")

redeem_sigs = []
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
redeem_sigs.append(redeem_sig_1)
redeem_sigs.append(redeem_sig_2)
redeem_sigs.append(redeem_sig_3)

print("How do you want to proceed? You can:")
print("1 - Try to spend the above transaction without signing it (will fail)")
print("2 - Pick the parties to sign the transaction")
response = input()

if response == 1:
  print("Here is your unlocking Tx (it will not work since no one signed it):")
  print(f'Unlocking Tx:\n{encode_tx(redeem_tx)}')
else:
  first_party_to_sign = None
  second_party_to_sign = None

  # First party to sign:
  while first_party_to_sign not in [1, 2, 3]:
    first_party_to_sign = input("\nPick which party will sign the multisig first (1, 2, or 3):\n")
    try:
      first_party_to_sign = int(first_party_to_sign)
    except ValueError as e:
      print("Please pick either party 1, 2, or 3 to sign the transaction.")
      continue
    
    if first_party_to_sign not in [1, 2, 3]:
      print("Please pick either party 1, 2, or 3 to sign the transaction.")
  print("Party", first_party_to_sign, "signed the transaction!")
  
  redeem_tx_copy = deepcopy(redeem_tx)
  redeem_tx_copy['vin'][0]['witness'] = [ 0, redeem_sigs[first_party_to_sign-1], redeem_script ]
  print(f'\nAt this point, the redeem transaction would look like the following and it would be invalid since it only had one of the 3 signatures.')
  print(f'Feel free to sendrawtransaction to prove it will not redeem:\n{encode_tx(redeem_tx_copy)}')
  
  second_party_to_sign = first_party_to_sign
  while first_party_to_sign == second_party_to_sign or second_party_to_sign not in [1, 2, 3]:
    second_party_to_sign = input("\nPick which party will sign the multisig second (1, 2, or 3):\n")
    try:
      second_party_to_sign = int(second_party_to_sign)
    except ValueError as e:
      print("Please pick either party 1, 2, or 3 to sign the transaction.")
      continue
    
    if second_party_to_sign not in [1, 2, 3]:
      print("Please pick either party 1, 2, or 3 to sign the transaction.")
    if first_party_to_sign == second_party_to_sign:
      print("First and second party are the same, please pick different parties.")
  print("Party", second_party_to_sign, "signed the transaction!")

  if first_party_to_sign < second_party_to_sign:
    redeem_tx['vin'][0]['witness'] = [ 0, redeem_sigs[first_party_to_sign-1], redeem_sigs[second_party_to_sign-1], redeem_script ]
  else:
    redeem_tx['vin'][0]['witness'] = [ 0, redeem_sigs[second_party_to_sign-1], redeem_sigs[first_party_to_sign-1], redeem_script ]
  print(f'\nFinal Valid Unlocking Tx:\n{encode_tx(redeem_tx)}')
  
  print("\nGoing to send the redeeming transaction now!")
  party1_rpc.send_transaction(redeem_tx)

  print("\nNow go mine a block and check your account balances to see the transfer.")

#redeem_tx['vin'][0]['witness'] = [ 0, redeem_sig_1, redeem_sig_2, redeem_sig_3, redeem_script ]
#redeem_tx['vin'][0]['witness'] = [ redeem_script, redeem_sig_3, redeem_sig_2, redeem_sig_1, 'OP_0' ]
#redeem_tx['vin'][0]['witness'] = [ 0, redeem_sig_1, redeem_sig_2, redeem_script ]

#print(f'Unlocking Tx:\n{encode_tx(redeem_tx)}')