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
There are several transaction types that are detailed in this repository and were tested on regtest and then used on testnet. Each of these transactions was generated "by hand" using Python, and then broadcast to the Bitcoin Test Network via JSON RPC calls to bitcoin core. The five transaction types are:
1. Pay-to-Public Key Hash (p2pkh)
2. Pay-to-Witness Public Key Hash (p2wpkh)
3. Pay-to-Witness Script Hash (p2wsh)
4. Multisig
5. Timelock

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
Output from testing on regtest:  
```
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./p2wpkh_final.py 
Enter wallet name: bergs-wallet
Enter amount to send (in satoshis): 1500000000
Enter fee in satoshis (or press enter for default 500): 
Using default fee of 500
Select one of the following options:
(a) Enter recipient address
(w) Enter recipient wallet name in bitcoin core:
a
Enter recipient payment segwit address: bcrt1q00zuj3ufkllt6fejmkf0eyx5zrape80ahjy0m4

## Pay-to-Witness-Pubkey-Hash Example ##

-- Transaction Id --
efff8f37291ff7b87c774a44be598e044b597d4f8e3da2f7db62e359a931c84f

-- Transaction Hex --
010000000001010599318c7b02fc122f1003671854d21741a212c4eb25cc1735dd8c9574f620400000000000ffffffff02002f6859000000001600147bc5c94789b7febd2732dd92fc90d410fa1c9dfd0cc19dd000000000160014374453a3dbc719a0271da6853b8d04785c4cd1660247304402203792c7f9acdc817e8d7ccad8a6ccae51794508222c099ac44267c9864abafccc0220280a2fce7999677cd9146b180493fefca998d43e14b41e077c6c6c8164976ba5012102f8ef2d77f50645b896eb199f3809b22cbfda1032229b8975b3e41e9544be9ae600000000
```

![Bergs Wallet](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/images/p2wpkh_bergs_wallet_send.png)   
![Bob Wallet](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/images/p2wpkh_bob_wallet_receive.png)   

Testnet:  
[Testnet Transaction Link](https://mempool.space/testnet/tx/cb6b790377bf8c8c430dad59de18c6b9f6caed319008e38581ace2eed3b4b2e0)  
Console Output:  
```
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./p2wpkh_final.py 
Enter wallet name: bergs-testnet
Enter amount to send (in satoshis): 2222
Enter fee in satoshis (or press enter for default 500): 
Using default fee of 500
Select one of the following options:
(a) Enter recipient address
(w) Enter recipient wallet name in bitcoin core:
a
Enter recipient payment segwit address: tb1q2k2y0lnl86sfh3gmkkrf4mqjr2u75w9w3hu39h

## Pay-to-Witness-Pubkey-Hash Example ##

-- Transaction Id --
cb6b790377bf8c8c430dad59de18c6b9f6caed319008e38581ace2eed3b4b2e0

-- Transaction Hex --
010000000001016ef242562f7c2c9b183f901801bb8a917e5b866a83b8a79a4fd5ab112c8b5c350000000000ffffffff02ae08000000000000160014559447fe7f3ea09bc51bb5869aec121ab9ea38ae3606000000000000160014c0efedcb577f2b90f39cb549d64a72cec34023eb02483045022100eca0c1619622592f5c453441c61478f82d4fa83d538e46bedd420a38ddc3757a02200406c93472cf751ed81f049700d300143a8ec171d9fb404d7658d14919b9fdf8012103bfbf0291f09a86b2d44d346194d5d7e61dfb89494c6abaf31d163221874e58b700000000
```

## Pay-to-Witness Script Hash (p2wsh)
Output from testing on regtest (note the script automatically sends the transaction via JSON RPC call):  
```
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./p2wsh_final.py 
Enter wallet name: bergs-wallet
Enter amount to send (in satoshis): 1000000000
Enter fee in satoshis (or press enter for default 500): 
Using default fee of 500
Enter your secret: sup3rS3cr3t

# Pay-to-Witness-Script-Hash Example

Locking Txid:
8ab3dae6ad29483024c114c2a2f1ed26ee0e0bda46374e93a65844f4711d35f3

Redeem Script:
a914d8a126c4cf5b76ace0966a7ace2f033976880efc8876a914a3785e0a1552225cd770ae9dd941c8f0f4f3496988ac

Locking Tx:
010000000001010499f91d2d18582c32d246cb2ba0376149e3605b59062f7110b9ac516771c1c10000000000ffffffff0200ca9a3b0000000022002070e92302f26940554341396a5f5659d50f6c28397d0c1e1e0bfdf75423b5883f0c266bee000000001976a9141a7faeb7bc1e3fcb7af7dd26af9973879b20083d88ac0247304402200beb0046fc0d92a5bd86ce644243c6e3f288f85c92ba150465e7f5a8e2aeaf4a0220018806322bb4bddd096e2322addbe60d53842e1f593262b4140ca4b147fca858012102f8ef2d77f50645b896eb199f3809b22cbfda1032229b8975b3e41e9544be9ae600000000

Unlocking Tx:
01000000000101f3351d71f44458a6934e3746da0b0eee26edf1a2c214c124304829ade6dab38a0000000000ffffffff010cc89a3b00000000160014a3785e0a1552225cd770ae9dd941c8f0f4f3496904473044022067a0d24a4a7f12b07a06a0a0ac85854262e7b571b91f96a3cfa1803bbb2e07ed02205f00be53c496633310f4ab90cdac1e060202dfb7bf931785884d6e0d0ba3c77501210366c3263443b490702393532bed9e5cd3e1ad0a75710b53b4bd494bba4a670d550b737570337253336372337430a914d8a126c4cf5b76ace0966a7ace2f033976880efc8876a914a3785e0a1552225cd770ae9dd941c8f0f4f3496988ac00000000
```

And finally the screeshots showing bergs-wallet and bob-wallet and the 1BTC transaction:  
![Bergs Wallet](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/images/p2wsh_bergs_wallet.png)   

Testnet:  
[Funding Testnet Transaction Link](https://mempool.space/testnet/tx/69e656fc6f827accf1d1ade12830ea1242fefaf3999d4081ab72e3d19ff7edd1)  
[Redeeming Testnet Transaction Link](https://mempool.space/testnet/tx/9858f8c4c0f0bef60a26e36c3865bb8ccc06ecdf5d03187062d04b438ee050f6)  
Console Output:   
```
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./p2wsh_final.py 
Enter wallet name: bergs-testnet
Enter amount to send (in satoshis): 2000
Enter fee in satoshis (or press enter for default 500): 
Using default fee of 500
Enter your secret: testS3cret
SCRIPT HERE: 44c46b2643ca8cd7c6983d12f5185a1e6d544c6a

# Pay-to-Witness-Script-Hash Example

Locking Txid:
69e656fc6f827accf1d1ade12830ea1242fefaf3999d4081ab72e3d19ff7edd1

Redeem Script:
a914dd62e2a7610e7e2143065c198a1fefe6596d992c8876a914a1c9e52a87c3b6e8f0bd3f734da9d42c7af3585188ac

Locking Tx:
01000000000101502865ba0b8e9d569e331d7c159742f6ea561c1e71be94f92398b982cec2896a0000000000ffffffff02d007000000000000220020328911ea8702fcc9092198fb5b5367ca6e8a7a6b207bf7557d36685d7e5266c44c1d0000000000001976a91464a2829a3937da00a7c3a929da7fbf7c77ca532988ac02483045022100f3cab7691752e757709044555925c4d73fcbae25731a67afeb6b3027973c836b022032fdfc94b1f7723e523ba4f966c5fc4a5867f613d0f516c4e29efffb2e67db5a012102de6f8a797d2d9df4f9801ce5eb26ffdeabf41d022a74c2e8d308cc2bd5bb75e300000000

Unlocking Tx:
01000000000101d1edf79fd1e372ab81409d99f3fafe4212ea3028e1add1f1cc7a826ffc56e6690000000000ffffffff01dc05000000000000160014a1c9e52a87c3b6e8f0bd3f734da9d42c7af35851044730440220040da7f0362c3f74880975ca9a443dff27cc77b555e385559eee6c579faeed79022014a48f021fa6a7227f92dc8e4e493224f2b6758c9aee94847fa5c9340a153061012102ece4521a83e3f569fa3119adbbd63e3722b1c5008318365ceb2954da3c0ac0400a7465737453336372657430a914dd62e2a7610e7e2143065c198a1fefe6596d992c8876a914a1c9e52a87c3b6e8f0bd3f734da9d42c7af3585188ac00000000
```


## Multisig
Regtest output here.

Link to testnet transaction.

## Timelock
Regtest output here.

Link to testnet transaction.
