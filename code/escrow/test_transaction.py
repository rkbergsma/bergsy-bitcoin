#!/usr/bin/env python3
import json, os, sys

# sys.path.append(os.path.dirname(__file__).split('/transactions')[0])
sys.path.insert(1, os.path.abspath(".."))

from copy import deepcopy

from lib.hash     import hash160
from lib.sign     import sign_tx
from lib.encoder  import encode_tx, encode_script
from lib.helper   import hash_script, get_txid, decode_address
from lib.rpc      import RpcSocket

def intro():
  print("Welcome to the escrow tutorial! \
    In this tutorial, we will facilitate the transaction between two parties, \
    a buyer and a seller. Neither party trusts the other, so we will enlist the help \
    of an arbitrator.")

def set_widget_amount():
  widget_price = input("Set the price of the widget, in satoshis:")
  try:
    return int(widget_price)
  except ValueError:
    raise Exception("Please enter a price in Satoshis (int)!")

def get_wallets():
  buyer_wallet = input('Enter buyer wallet name:')
  buyer = RpcSocket({ 'wallet': buyer_wallet})
  assert buyer.check()

  seller_wallet = input('Enter seller wallet (used to get pubkey for signing):')
  seller = RpcSocket({ 'wallet': seller_wallet})
  assert seller.check()

  arbitrator_wallet = input('Enter arbitrator wallet name:')
  arbitrator = RpcSocket({ 'wallet': arbitrator_wallet})
  assert arbitrator.check()

  return buyer, seller, arbitrator

def verify_buyer_funds(buyer, price):
  i = 0
  utxo_sum = 0
  utxo_list = []
  while utxo_sum < price:
    utxo = buyer.get_utxo(i)
    utxo_list.append(utxo)
    utxo_sum = utxo_sum + utxo['value']
    i = i + 1
  return utxo_list

def generate_locking_script(buyer_recv, seller_recv, arbitrator_recv):
  print("Generating locking script for transaction:")
  script_words = [
      'OP_2',
      buyer_recv['pub_key'],
      seller_recv['pub_key'],
      arbitrator_recv['pub_key'],
      'OP_3',
      'OP_CHECKMULTISIG'
  ]
  print(script_words)
  return script_words

def generate_vin(utxo_list):
  vins = []
  for utxo in utxo_list:
    vin = {
          'txid': utxo['txid'],
          'vout': utxo['vout'],
          'script_sig': [],
          'sequence': 0xFFFFFFFF
        }
    vins.append(vin)
  return vins

if __name__ == "__main__":
  # Setup
  intro()
  price = set_widget_amount()
  buyer, seller, arbitrator = get_wallets()
  
  # Verify buyer funds and get utxo that will be used to fund transaction
  buyer_utxo = verify_buyer_funds(buyer, price)

  # Get seller receiving key and address
  print("Generating receive addresses for transaction")
  buyer_recv = buyer.get_recv()
  seller_recv = seller.get_recv()
  arbitrator_recv = arbitrator.get_recv()

  ## Get a change address for Buyer.
  buyer_pubkey_hash  = decode_address(buyer_recv['address'])

  # Generate locking script
  locking_script = generate_locking_script(buyer_recv, seller_recv, arbitrator_recv)

  ## We hash the above program with a sha256. This will lock the
  ## output to accept the program script which matches the hash.
  script_hash = hash_script(locking_script, fmt='sha256')

  ## This is the hex-encoded script that we will present in order to 
  ## unlock and spend the output. It should decode to match the script hash.
  witness_script = encode_script(locking_script, prepend_len=False).hex()

  ## This is the total value of the locking script.
  tx_fee = 1000
  total_value = sum(utxo['value'] for utxo in buyer_utxo) - tx_fee
  print("Total value of transaction:", total_value)

  ## Generate vin
  vin = generate_vin(buyer_utxo)

  ## The locking transaction. This tx spends the participant utxos.
  locking_tx = {
      'version': 1,
      'vin': vin,
      'vout': [{
          'value': price,
          'script_pubkey': [ 0, script_hash ]
      },
      {
          'value': total_value - price,
          'script_pubkey': ['OP_DUP', 'OP_HASH160', buyer_pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
      }
      ],
      'locktime':0
  }

  ## Get txid for the locking script.
  locking_raw  = encode_tx(locking_tx)
  locking_txid = get_txid(locking_raw)

  ## Each participant signs the locking transaction.
  buyer_signs_transaction = input("Confirm buyer signs locking transaction (y/n):")
  if buyer_signs_transaction == 'y':
    for index, utxo in enumerate(buyer_utxo):
      buyer_signature = sign_tx(
        locking_tx, 
        index, 
        utxo['value'], 
        utxo['pubkey_hash'], 
        utxo['priv_key']
      )
      locking_tx['vin'][index]['witness'] = [ buyer_signature, utxo['pub_key'] ]

  print(f'''
  Locking Tx:
  {json.dumps(locking_tx, indent=2)}

  Locking Txid:
  {locking_txid}

  Locking Tx Value:
  {total_value}

  Locking Tx Hex:
  {encode_tx(locking_tx)}

  Witness hash:
  {script_hash}

  Witness Program:
  {witness_script}
  ''')


  sys.exit()


  ## The locking transaction. This tx spends the participant utxos.
  locking_tx = {
      'version': 1,
      'vin': [
        {
          'txid': alice_utxo['txid'],
          'vout': alice_utxo['vout'],
          'script_sig': [],
          'sequence': 0xFFFFFFFF
        },
        {
          'txid': bob_utxo['txid'],
          'vout': bob_utxo['vout'],
          'script_sig': [],
          'sequence': 0xFFFFFFFF
        }
      ],
      'vout': [{
          'value': total_value,
          'script_pubkey': [ 0, script_hash ]
      }],
      'locktime':0
  }

  ## Get txid for the locking script.
  locking_raw  = encode_tx(locking_tx)
  locking_txid = get_txid(locking_raw)

  ## Each participant signs the locking transaction.
  alice_signature = sign_tx(
    locking_tx, 
    0, 
    alice_utxo['value'], 
    alice_utxo['pubkey_hash'], 
    alice_utxo['priv_key']
  )

  bob_signature = sign_tx(
    locking_tx, 
    1, 
    bob_utxo['value'], 
    bob_utxo['pubkey_hash'], 
    bob_utxo['priv_key']
  )

  ## Add the signatures and pubkeys to the witness field.
  locking_tx['vin'][0]['witness'] = [ alice_signature, alice_utxo['pub_key'] ]
  locking_tx['vin'][1]['witness'] = [ bob_signature, bob_utxo['pub_key'] ]

  print(f'''
  Locking Tx:
  {json.dumps(locking_tx, indent=2)}

  Locking Txid:
  {locking_txid}

  Locking Tx Value:
  {total_value}

  Locking Tx Hex:
  {encode_tx(locking_tx)}

  Witness hash:
  {script_hash}

  Witness Program:
  {witness_script}
  ''')

  ## Setup a redeem transaction.
  redeem_tx = {
      'version': 1,
      'vin': [
        {
          'txid': locking_txid,
          'vout': 0,
          'script_sig': [],
          'sequence': 0xFFFFFFFF
        },
      ],
      'vout':[
          {
            'value': total_value - tx_fee,
            'script_pubkey': []
          },
      ]
  }

  ## Configure redeem TX for Alice
  alice_tx = deepcopy(redeem_tx)
  alice_tx['vout'][0]['script_pubkey'] = [ 0, alice_recv['pubkey_hash'] ]
  alice_sig = sign_tx(alice_tx, 0, total_value, witness_script, alice_recv['priv_key'])
  alice_tx['vin'][0]['witness'] = [
    alice_sig,
    'ab' * 32, 
    '01', 
    witness_script
  ]

  ## Configure redeem TX for Bob.
  bob_tx = deepcopy(redeem_tx)
  bob_tx['vout'][0]['script_pubkey'] = [ 0, bob_recv['pubkey_hash'] ]
  bob_sig = sign_tx(bob_tx, 0, total_value, witness_script, bob_recv['priv_key'])
  bob_tx['vin'][0]['witness'] = [
    bob_sig,
    'ab' * 31 + 'ac', 
    0, 
    witness_script
  ]

  print(f'''
  Alice's Redeem Tx:
  {json.dumps(alice_tx, indent=2)}

  Alice's Redeem Tx Hex:
  {encode_tx(alice_tx)}

  Bob's Redeem Tx:
  {json.dumps(bob_tx, indent=2)}

  Bob's Redeem Tx Hex:
  {encode_tx(bob_tx)}
  ''')
