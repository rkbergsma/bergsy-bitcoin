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
Output from testing on regtest:  
```
// Use the -l option to create the locking transaction. You will need the pubkeys of the addresses of the two other participants.
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./multisig_final.py -l
Enter wallet name to fund multisig: bergs-wallet
Enter amount to send (in satoshis): 1000000000
Enter fee in satoshis (or press enter for default 500): 
Using default fee of 500
Enter recipient pubkey: 034c8081617ee9df9caee1442af268cbdd21dc46fab499c64b3f301ff006dfd15c  // one of the multisig participants generates an address and provides the pubkey to the creator
Enter recipient pubkey: 03349855b54e14016468177a8dd60ba448c935207ac7ae720e98249f6a984a6d2b  // other multisig participant generates an address and provides the pubkey to the creator
Party 1 Address: bcrt1qacqf4mrwt6lmghedcrqdlnhs8lnntcg4jpd6xp

    ## Pay-to-Witness-Pubkey-Hash Example ##

    -- Transaction Id --
    3eefc34cd19bca11c4e5972c5b81f8c4ac6ade88f797d41e131afd749bacd5b1

    -- Transaction Hex --
    010000000001010d17f8ee57fa376bd517caf7325ff8e2f61408279bc2756d8481c1a4200866b40000000000ffffffff0200ca9a3b00000000220020a362b080c6051a59697f04fb4e4c1420a52f267424dac340058f82971a3a57510c266bee000000001600149be7629ae11e3ee8c0c0bda3370c872af3385e6a0248304502210091c891ceabf02f4d229a80320ea8b578fc3672037db62f7b70aabdb38bea054002204de74e699e521c69392dc87c0a1f27358c72d695dc51803bbc5a0787a2c1f202012102f8ef2d77f50645b896eb199f3809b22cbfda1032229b8975b3e41e9544be9ae600000000
    
Generating psbt redeem TX.
Enter party 1 address: bcrt1qacqf4mrwt6lmghedcrqdlnhs8lnntcg4jpd6xp
Enter party 2 address: bcrt1qlgj3mhnwh2gamkcnz0v7xchy6v0393htssnvx4
Enter party 3 address: bcrt1q55ydpczp7gs88vmtxp7j9p8ak3jjcwngn0rsxd
Writing file psbt.json                                                                 // this psbt.json can be sent to any multisig participant to sign

// Contents of psbt.json
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ cat psbt.json 
{"redeem_script": "522102bf904657a784807a14716714b4ce217de79c799d325dc02247f856479977b53621034c8081617ee9df9caee1442af268cbdd21dc46fab499c64b3f301ff006dfd15c2103349855b54e14016468177a8dd60ba448c935207ac7ae720e98249f6a984a6d2b53ae", "amount": 1000000000, "redeem_tx": {"version": 1, "vin": [{"txid": "3eefc34cd19bca11c4e5972c5b81f8c4ac6ade88f797d41e131afd749bacd5b1", "vout": 0, "script_sig": [], "sequence": 4294967295}], "vout": [{"value": 333332333, "script_pubkey": [0, "ee009aec6e5ebfb45f2dc0c0dfcef03fe735e115"]}, {"value": 333333333, "script_pubkey": [0, "fa251dde6eba91dddb1313d9e362e4d31f12c6eb"]}, {"value": 333333333, "script_pubkey": [0, "a508d0e041f22073b36b307d2284fdb4652c3a68"]}], "locktime": 0}}

// Use the -s option to sign the transaction, with -p pointing to the psbt file
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./multisig_final.py -s -p psbt.json
Reading in psbt: psbt.json
Enter wallet name to connect for RPC: test-wallet
Enter address you are signing for: bcrt1qlgj3mhnwh2gamkcnz0v7xchy6v0393htssnvx4
Please enter index of your signature: 1
Writing file psbt_signed.json                    // send this psbt_signed.json to any other participant to be get at least one more signature

// Use the -s option to sign the transaction, with -p pointing to the psbt file
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./multisig_final.py -s -p psbt_signed.json
Reading in psbt: psbt_signed.json
Enter wallet name to connect for RPC: bergs-wallet
Enter address you are signing for: bcrt1qacqf4mrwt6lmghedcrqdlnhs8lnntcg4jpd6xp
Please enter index of your signature: 0
Writing file psbt_signed.json

// Use the -r option to create the final redeem transaction which contains at least 2 signatures
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./multisig_final.py -r -p psbt_signed.json
Enter wallet name to connect for RPC: bergs-wallet
Reading in psbt: psbt_signed.json

Final Valid Unlocking Tx:
01000000000101b1d5ac9b74fd1a131ed497f788de6aacc4f8815b2c97e5c411ca9bd14cc3ef3e0000000000ffffffff036d3fde1300000000160014ee009aec6e5ebfb45f2dc0c0dfcef03fe735e1155543de1300000000160014fa251dde6eba91dddb1313d9e362e4d31f12c6eb5543de1300000000160014a508d0e041f22073b36b307d2284fdb4652c3a680400483045022100fca72c04c0f770481675d0d8b8fc52f842fee4757e331d34dde6248b4a7d611802204c38260edfcd3224a84915e2788451aef74a5dc911dfa91e4c4f3621c8d9a4b801483045022100a73eea74686fa5d3baa06cdcabec8d87d0aed77980f6e68bec4d7943c1a052aa02204243a051b92ea773b99c028cc20f14cf75e24d8085f7d5aa2cf3f3b72ed621a70169522102bf904657a784807a14716714b4ce217de79c799d325dc02247f856479977b53621034c8081617ee9df9caee1442af268cbdd21dc46fab499c64b3f301ff006dfd15c2103349855b54e14016468177a8dd60ba448c935207ac7ae720e98249f6a984a6d2b53ae00000000
Would use rpc to send transaction here
```

Here are some screenshots from each wallet showing the 10 BTC from bergs-wallet funding the multisig, followed be the outputs being split equally among all participants.
![Bergs Wallet](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/images/multisig_bergs_wallet.png)  
![Test Wallet](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/images/test_bergs_wallet.png)  
![Bob Wallet](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/images/multisig_bob_wallet.png)  


Testnet:  
[Funding Testnet Transaction Link](https://mempool.space/testnet/tx/efd2a34110a9338d3e64d3316a49e61c157f32b530ca0bffb47f603a8d3d8bcd)   
[Redeeming Testnet Transaction Link](https://mempool.space/testnet/tx/8b9a817247f1034c963d1794a28e4df98425f302c9588044ae343c22eef6fe1a)    

First, Ryan created and funded the transaction:
```
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./multisig_final.py -l
Enter wallet name to fund multisig: bergs-testnet
Enter amount to send (in satoshis): 300000
Enter fee in satoshis (or press enter for default 500): 
Using default fee of 500
Enter recipient pubkey: 03d166217f748de03cad6ec51bb10825ff434f5d0aeefa9e8d0dc186c3d934f959
Enter recipient pubkey: 029ec0efa801cab42933fca5dbc2d18d9c67ed4bee4e2b26b8e5d4cc0433a195b3
Party 1 Address: tb1ql5sqz72a3s9ezn66zcnut9lq6jvsglj963j93f

    ## Pay-to-Witness-Pubkey-Hash Example ##

    -- Transaction Id --
    efd2a34110a9338d3e64d3316a49e61c157f32b530ca0bffb47f603a8d3d8bcd

    -- Transaction Hex --
    01000000000101156e71b23f2ed7928936cf64938265b421a1ef699820ac3c03156539223dd0bd0000000000ffffffff02e093040000000000220020bcaaf11b3c74b80377fccba2d9779679872eff40798ddb056da1228b6228ab64a331130000000000160014b41e50257cf019c95da627043d95dd93e196805d02483045022100a248cbb0ad0a9338c5c503fa698e305bbbe54dee9173d7ad14f4bc1cfa0d87e802201b06832a94a8e4501044ffe4c2ad7782396325518401826a1ca54501a9f587b00121032bfd360b1b1995bd3814519e7d2099ec9cbe04fd0e9ffe9ec985faf919f9abf100000000
    
Generating psbt redeem TX.
Enter party 1 address: tb1ql5sqz72a3s9ezn66zcnut9lq6jvsglj963j93f
Enter party 2 address: tb1q6mqeq3gkekepp6f8nza2sptwkqks0qp4hja8tj
Enter party 3 address: tb1q6z4n62j6xjcvjyps4gwzcadyw6gk4cwxfwm6h7
Writing file psbt.json
```

Then, Ryan sent Jeff the psbt.json and Jeff signed the transaction:
```
jtipps@DESKTOP-J69RTBS:~/GitRepos/bergsy-bitcoin/code/transactions$ ./multisig_final.py -s -p psbt.json
Reading in psbt: psbt.json
Enter wallet name to connect for RPC: tn_wallet
Enter address you are signing for: tb1q6mqeq3gkekepp6f8nza2sptwkqks0qp4hja8tj
Please enter index of your signature: 1
Writing file psbt_signed.json
```

Then, Jeff sent Bob the psbt_signed.json and Bob signed it:
```
(bitcoin) ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/transactions$ ./multisig_final.py -s -p psbt_signed.json 
Reading in psbt: psbt_signed.json
Enter wallet name to connect for RPC: bob-testnet
Enter address you are signing for: tb1q6z4n62j6xjcvjyps4gwzcadyw6gk4cwxfwm6h7
Please enter index of your signature: 2
Writing file psbt_signed.json
```

Then, Jeff sent the fully signed psbt_signed.json back to Jeff for him to broadcast it:
```
jtipps@DESKTOP-J69RTBS:~/GitRepos/bergsy-bitcoin/code/transactions$ ./multisig_final.py -r -p psbt_signed.json
Enter wallet name to connect for RPC: tn_wallet
Reading in psbt: psbt_signed.json

Final Valid Unlocking Tx:
01000000000101cd8b3d8d3a607fb4ff0bca30b5327f151ce6496a31d3643e8d33a91041a3d2ef0000000000ffffffff03b882010000000000160014fd2001795d8c0b914f5a1627c597e0d499047e45a086010000000000160014d6c1904516cdb210e92798baa8056eb02d078035a086010000000000160014d0ab3d2a5a34b0c91030aa1c2c75a476916ae1c60400483045022100b51cc5a916ca0473a07a7f56d77c3ead2a6594e9221f99311028267e5ea8b1f3022002c068c0087e40df6c4b6d580029a7c01e20ade226ba6129bd609ca9a617919501483045022100c2aa12a55c35e6c92092ed3786873f16cf00ce45673823711d56a6776cd6013f0220409b55993aa4ccc44937efe50f29e8c5f2f5b4b2a8557dfb899c5dcd77d1bd95016952210344cf6ea9b9d91e38c15a09a37be5d6675e710277db52295a2dd10079a7be00672103d166217f748de03cad6ec51bb10825ff434f5d0aeefa9e8d0dc186c3d934f95921029ec0efa801cab42933fca5dbc2d18d9c67ed4bee4e2b26b8e5d4cc0433a195b353ae00000000
Would use rpc to send transaction here
```


## Timelock
See Bitbnb for example timelock transactions implemented: https://github.com/rkbergsma/Bitbnb.
