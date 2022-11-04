# Assignment 01 - Bitcoin Transaction

The purpose of this assignment is to demonstrate that you can construct a valid bitcoin transaction, and broadcast it successfully on the Bitcoin Test Network.

## Requirements

* A document or script within your repository, which shows your work in both constructing, and broadcasting the transaction.

* The transaction ID of the Bitcoin transaction, on the Bitcoin Testnet network. It should be publicly viewable on a Blockchain explorer, such as [mempool.space](https://mempool.space/testnet).

## Resources

**Bitcoin Testnet Faucet**  
https://bitcoinfaucet.uo1.net

**Mempool.space Testnet**  
https://mempool.space/testnet

## Solution
There are several transaction types that are detailed in this repository and were tested on regtest and then used on testnet. Each of these transactions was generated "by hand" using Python, and then broadcast to the Bitcoin Test Network via JSON RPC calls to bitcoin core.

## Pay-to-Public Key Hash (p2pkh)
Output from testing on regtest:  
```
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./p2pkh_final.py
Enter wallet name: bergs-wallet 
Enter amount to send (in satoshis): 100000000
Enter fee in satoshis (or press enter for default 1000): 
Using default fee of 1000
Select one of the following options:
(a) Enter recipient address
(w) Enter recipient wallet name in bitcoin core:
w
Enter recipient wallet name: bob-wallet

## Pay-to-Pubkey-Hash Example ##

-- Transaction Id --
55ec3cb21ffa062680a8e3326360a869a1c7ac5f9158631d52226585347bdbc1

-- Transaction Hex --
010000000001010050fcabc44cc1f9c711240ee9becac9738d9b1b4c958bc7f3e37e9d77dd7cc30000000000ffffffff0200e1f505000000001976a9140d21c85ad775a1fde0af5697d25fbca8a9984f3c88ac180d1024010000001976a914ed390bac763976c7608362d8f51cdd4fd752e10b88ac02483045022100e68cfddf9f6f87976b023d25fd1d62096b8fa911b716e1bdeedbf6fb582282fe02206a6717781aa02c472876c556c53da5c9ab2d7294cbfe0b4e88656c474f4780b3012102f8ef2d77f50645b896eb199f3809b22cbfda1032229b8975b3e41e9544be9ae600000000

Would send transaction here
```

Then, in bitcoin core:
```
14:27:01
decoderawtransaction 010000000001010050fcabc44cc1f9c711240ee9becac9738d9b1b4c958bc7f3e37e9d77dd7cc30000000000ffffffff0200e1f505000000001976a9140d21c85ad775a1fde0af5697d25fbca8a9984f3c88ac180d1024010000001976a914ed390bac763976c7608362d8f51cdd4fd752e10b88ac02483045022100e68cfddf9f6f87976b023d25fd1d62096b8fa911b716e1bdeedbf6fb582282fe02206a6717781aa02c472876c556c53da5c9ab2d7294cbfe0b4e88656c474f4780b3012102f8ef2d77f50645b896eb199f3809b22cbfda1032229b8975b3e41e9544be9ae600000000

14:27:01
{
  "txid": "55ec3cb21ffa062680a8e3326360a869a1c7ac5f9158631d52226585347bdbc1",
  "hash": "5a1657e96b3663ad78d2f1e2d655150bea2bb2a428adf6319ca79f93cc303ef6",
  "version": 1,
  "size": 229,
  "vsize": 147,
  "weight": 586,
  "locktime": 0,
  "vin": [
    {
      "txid": "c37cdd779d7ee3f3c78b954c1b9b8d73c9cabee90e2411c7f9c14cc4abfc5000",
      "vout": 0,
      "scriptSig": {
        "asm": "",
        "hex": ""
      },
      "txinwitness": [
        "3045022100e68cfddf9f6f87976b023d25fd1d62096b8fa911b716e1bdeedbf6fb582282fe02206a6717781aa02c472876c556c53da5c9ab2d7294cbfe0b4e88656c474f4780b301",
        "02f8ef2d77f50645b896eb199f3809b22cbfda1032229b8975b3e41e9544be9ae6"
      ],
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "value": 1.00000000,
      "n": 0,
      "scriptPubKey": {
        "asm": "OP_DUP OP_HASH160 0d21c85ad775a1fde0af5697d25fbca8a9984f3c OP_EQUALVERIFY OP_CHECKSIG",
        "hex": "76a9140d21c85ad775a1fde0af5697d25fbca8a9984f3c88ac",
        "address": "mgiPYojQQwtwvDSdMLmPVTmegKuDZiwM7i",
        "type": "pubkeyhash"
      }
    },
    {
      "value": 48.99999000,
      "n": 1,
      "scriptPubKey": {
        "asm": "OP_DUP OP_HASH160 ed390bac763976c7608362d8f51cdd4fd752e10b OP_EQUALVERIFY OP_CHECKSIG",
        "hex": "76a914ed390bac763976c7608362d8f51cdd4fd752e10b88ac",
        "address": "n39Gn7fDmXpGVW3pSRbhRrEkYn9h5yLWeX",
        "type": "pubkeyhash"
      }
    }
  ]
}

14:27:16
sendrawtransaction 010000000001010050fcabc44cc1f9c711240ee9becac9738d9b1b4c958bc7f3e37e9d77dd7cc30000000000ffffffff0200e1f505000000001976a9140d21c85ad775a1fde0af5697d25fbca8a9984f3c88ac180d1024010000001976a914ed390bac763976c7608362d8f51cdd4fd752e10b88ac02483045022100e68cfddf9f6f87976b023d25fd1d62096b8fa911b716e1bdeedbf6fb582282fe02206a6717781aa02c472876c556c53da5c9ab2d7294cbfe0b4e88656c474f4780b3012102f8ef2d77f50645b896eb199f3809b22cbfda1032229b8975b3e41e9544be9ae600000000

14:27:16
55ec3cb21ffa062680a8e3326360a869a1c7ac5f9158631d52226585347bdbc1

14:27:34
generatetoaddress 1 bcrt1qs3pclhlxwn2m25arahdw72wldgd90zqk3gjqks

14:27:34
[
  "7bbbdf1ab44df2288a2901a9f0489a05cf1ef7e60bdbf13ddf63c67f9bf9f92a"
]
```

And finally the screeshots showing bergs-wallet and bob-wallet and the 1BTC transaction:  
![Bergs Wallet](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/images/bergs_wallet_p2pkh.png)   
![Bob Wallet](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/images/bob_wallet_p2pkh.png)   


Testnet:  
[Testnet Transaction Link](https://mempool.space/testnet/tx/a79e43ff1304335d31995b15f2185957da4a28001fa41bcf0dc7beb9cd658ba0)
Console Output:  
```
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./p2pkh_final.py 
Enter wallet name: bergs-testnet
Enter amount to send (in satoshis): 5000
Enter fee in satoshis (or press enter for default 1000): 500
Select one of the following options:
(a) Enter recipient address
(w) Enter recipient wallet name in bitcoin core:
a
Enter recipient payment address: miQycgF36Rw1CH27uvkEPaADRUYAYzFVUq

## Pay-to-Pubkey-Hash Example ##

-- Transaction Id --
a79e43ff1304335d31995b15f2185957da4a28001fa41bcf0dc7beb9cd658ba0

-- Transaction Hex --
010000000001018ed4f2e4a71dc5b557e6b476b673a3273e53b1fe073ae3eccb95b1653616aa870000000000ffffffff0288130000000000001976a9141fc6fbffe3dc4d5d14eec562b2e5c60fa38e2b2588ac94110000000000001976a91423d579fc44220053f8de54c73f61df619533ccb788ac024730440220287b16f8f3206b8dd34626e38c96bde9f07c5b9bf336fe2b94abe6b3645d2e2302206858ddde6feaac795c731e0cfb5a6f0b262361e14822a4676c55436916419959012103a6e62d75d1d107fe8b969ed1b4437918bb2403083e1cfe97732fa8ffdb98e21100000000
```

## Pay-to-Witness Public Key Hash (p2wpkh)
Regtest output here.

Link to testnet transaction.

## Pay-to-Witness Script Hash (p2wsh)
Regtest output here.

Link to testnet transaction.

## Multisig
Regtest output here.

Link to testnet transaction.

## Timelock
Regtest output here.

Link to testnet transaction.
