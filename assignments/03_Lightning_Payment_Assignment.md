# Assignment 03 - Lightning Payment

The purpose of this assignment is to demonstrate that you can start a lightning node, open a channel with another peer, send a payment, and close the channel.

## Requirements

* A document or script within your repository, which shows your work in setting up a lightning node, opening a channel, sending a payment, and closing the channel.

* The transaction ID of the lightning "channel" transaction, on the Bitcoin Testnet network. It should be publicly viewable on a Blockchain explorer, such as [mempool.space](https://mempool.space/testnet).

## Examples

You will find some examples of how to start a lightning node in the `lnd-demo` folder. Feel free to use any software implementation of Lightning, such as LND, Core Lightning, Eclair, etc.

## Resources

**Lightning Network Daemon (LND)**  
https://github.com/lightningnetwork/lnd

**Core Lightning (CLN)**  
https://github.com/ElementsProject/lightning

**Eclair (Scala Lightning Node)**  
https://github.com/ACINQ/eclair

**Polar: One-click Lightning Network**  
https://github.com/jamaljsr/polar

**Bitcoin Testnet Faucet**  
https://bitcoinfaucet.uo1.net

**Mempool.space Testnet**  
https://mempool.space/testnet


## Solution
I set up two lighning nodes as Alice and Bob, as outlined in the lnd-demo in the bitcoin-programming github. I first performed this on regtest, and then testnet.  

Running the demo requires 4 main terminals:
1. lnd for Alice (runs and holds terminal)
2. lcli (wrapper for lncli) commands for Alice
3. lnd for Bob (runs and holds terminal)
4. lcli (wrapper for lncli) commands for Bob

### Regtest:
The 4 full logs for Regtest are located here:  
![Alice lnd](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/logs/alice_lnd_regtest.log)  
![Alice lcli](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/logs/alice_lcli_regtest.log)  
![Bob lnd](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/logs/bob_lnd_regtest.log)  
![Bob lcli](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/logs/bob_lcli_regtest.log)  

The sequence below highlights the overall flow of events:
```
// Alice starts her lnd node:
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/alice$ ./lnd --configfile=lnd.conf
Attempting automatic RPC configuration to bitcoind
Automatically obtained bitcoind's RPC credentials
2022-11-09 23:09:53.906 [INF] LTND: Version: 0.15.3-beta commit=v0.15.3-beta, build=production, logging=default, debuglevel=info
2022-11-09 23:09:53.906 [INF] LTND: Active chain: Bitcoin (network=regtest)
...

// Alice creates wallet
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/alice$ ./lcli create
Input wallet password: 
Confirm password: 

Do you have an existing cipher seed mnemonic or extended master root key you want to use?
Enter 'y' to use an existing cipher seed mnemonic, 'x' to use an extended master root key 
or 'n' to create a new seed (Enter y/x/n): n
...

// Bob starts his lnd node: 
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lnd --configfile=lnd.conf
Attempting automatic RPC configuration to bitcoind
Automatically obtained bitcoind's RPC credentials
2022-11-09 23:12:38.113 [INF] LTND: Version: 0.15.3-beta commit=v0.15.3-beta, build=production, logging=default, debuglevel=info
2022-11-09 23:12:38.113 [INF] LTND: Active chain: Bitcoin (network=regtest)
...

// Bob creates wallet
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lcli create
Input wallet password: 
Confirm password: 

Do you have an existing cipher seed mnemonic or extended master root key you want to use?
Enter 'y' to use an existing cipher seed mnemonic, 'x' to use an extended master root key 
or 'n' to create a new seed (Enter y/x/n): n
...

// Alice creates new send address and address funded via Bitcoin core:
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/alice$ ./lcli newaddress p2wkh
{
    "address": "bcrt1q5fh2fqa0fn7xu0z9zc3fuzcmgxlhl4ge5d437r"
}

// Bob creates new send address and address funded via Bitcoin core:
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lcli newaddress p2wkh
{
    "address": "bcrt1q5m2ud78lmtdmm3qy5237q0078guwt4n3pvn9d6"
}

// Get info of Bob's node (identity_pubkey) to add to Alice's wallet to connect and create channel
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lcli getinfo
{
    "version": "0.15.3-beta commit=v0.15.3-beta",
    "commit_hash": "b4e7131bdb47531ad2f00ce345ddcdb58935bba5",
    "identity_pubkey": "028ee94405efb9f3bacdc285db7116f8c34f1ea220999dd672facaa81795038192",
    "alias": "bob",
    "color": "#3399ff",
    "num_pending_channels": 0,
    "num_active_channels": 0,
    "num_inactive_channels": 0,
...

// Alice connect with Bob
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/alice$ ./lcli connect 028ee94405efb9f3bacdc285db7116f8c34f1ea220999dd672facaa81795038192@localhost:9737
{

}

// Alice start channel with Bob
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/alice$ ./lcli openchannel --node_key=028ee94405efb9f3bacdc285db7116f8c34f1ea220999dd672facaa81795038192 --local_amt=1000000
{
	"funding_txid": "98a174dc7e80789d3a19adc4078c59e41c7fe1480decd8242bdf5db7268dc45e"
}

// Bob checks and sees remote balance on Alice's end
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lcli channelbalance
{
    "balance": "0",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "remote_balance": {
        "sat": "996530",
        "msat": "996530000"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Bob creates invoice 
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lcli addinvoice --amt=10000
{
    "r_hash": "f06d8fe2e5827f88bcffbc1f4b4e58a261d53b6e6a09274dd072325832108b1f",
    "payment_request": "lnbcrt100u1p3kezdapp57pkclch9sflc308lhs05knjc5fsa2wmwdgyjwnwswge9svss3v0sdqqcqzpgxqyz5vqsp5m8de8q5nwcw0g3m4whs4e6arv9h5rwgvhjf4qtewrf36468uc8js9qyyssqh9czh4q5yzgr6tjp5ujjc9e46kga3syfwaevy49hptyv8a8yaqp3q5n65f7e9m6na44h9kzxg9y7gy5a5s0n0ak8paz2lrw4p75j82gqp27rrv",
    "add_index": "1",
    "payment_addr": "d9db938293761cf4477575e15ceba3616f41b90cbc93502f2e1a63aae8fcc1e5"
}

// Alice pays invoice
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/alice$ ./lcli sendpayment --pay_req=lnbcrt100u1p3kezdapp57pkclch9sflc308lhs05knjc5fsa2wmwdgyjwnwswge9svss3v0sdqqcqzpgxqyz5vqsp5m8de8q5nwcw0g3m4whs4e6arv9h5rwgvhjf4qtewrf36468uc8js9qyyssqh9czh4q5yzgr6tjp5ujjc9e46kga3syfwaevy49hptyv8a8yaqp3q5n65f7e9m6na44h9kzxg9y7gy5a5s0n0ak8paz2lrw4p75j82gqp27rrv
Payment hash: f06d8fe2e5827f88bcffbc1f4b4e58a261d53b6e6a09274dd072325832108b1f
Description: 
Amount (in satoshis): 10000
Fee limit (in satoshis): 500
Destination: 028ee94405efb9f3bacdc285db7116f8c34f1ea220999dd672facaa81795038192
Confirm payment (yes/no): yes
+------------+--------------+--------------+--------------+-----+----------+-----------------+-------+
| HTLC_STATE | ATTEMPT_TIME | RESOLVE_TIME | RECEIVER_AMT | FEE | TIMELOCK | CHAN_OUT        | ROUTE |
+------------+--------------+--------------+--------------+-----+----------+-----------------+-------+
| SUCCEEDED  |        0.031 |        0.195 | 10000        | 0   |      416 | 404620279087104 | bob   |
+------------+--------------+--------------+--------------+-----+----------+-----------------+-------+
Amount + fee:   10000 + 0 sat
Payment hash:   f06d8fe2e5827f88bcffbc1f4b4e58a261d53b6e6a09274dd072325832108b1f
Payment status: SUCCEEDED, preimage: 84ac8ae5ecc17be8919a8ed77f933f827b129626114bd12275975c7befadfa0c

// Alice sees payment in channel balance
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/alice$ ./lcli channelbalance
{
    "balance": "986530",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "986530",
        "msat": "986530000"
    },
    "remote_balance": {
        "sat": "10000",
        "msat": "10000000"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Bob sees payment in channel balance
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lcli channelbalance
{
    "balance": "10000",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "10000",
        "msat": "10000000"
    },
    "remote_balance": {
        "sat": "986530",
        "msat": "986530000"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Bob closes channel
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lcli closechannel 98a174dc7e80789d3a19adc4078c59e41c7fe1480decd8242bdf5db7268dc45e
{
	"closing_txid": "f1da01e6681ece6685fa01ccb652aad7afa56983012fa6e4e0be72438f8f6fc9"
}

// Bob sees channel is closed
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lcli channelbalance
{
    "balance": "0",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Alice sees channel is closed
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/alice$ ./lcli channelbalance
{
    "balance": "0",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Bob sends coins from lightning node back to on-chain
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lcli sendcoins bcrt1qmfy0laf7x6nv502glx4w97rcqrrezay3ymcv3p 10000
{
    "txid": "039bdf0a2e21a9dc1365bc8eb8f841bc6c1a452a3d5e365559a636d407dcbd93"
}

```

### Testnet:
The 2 full logs for Regtest are located here:  
![Ryan lcli](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/logs/ryab_lcli_testnet.log)  
![Bob lcli](https://github.com/rkbergsma/bergsy-bitcoin/tree/master/assignments/logs/bob_lcli_testnet.log)  

Testnet Transaction:
Transaction to fund the lightning node: https://mempool.space/testnet/tx/2554e18528a4a9f4d1a75f0fc1b7b5294497b2191c26d3c8b11df4665603137b
Transaction to fund channel: https://mempool.space/testnet/tx/d9fa96e7eedee54fa3ed53bb631beb826aaf743a66b2238805125591562badc8
Transaction to close the channel: https://mempool.space/testnet/tx/19d0278a3f2e12d9789fe59eec1fc9ddae9e450316b3b0de473f79e10d0d713f

The sequence below highlights the overall flow of events:
```
// Ryan starts his lnd node:
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lnd --configfile=lnd.conf
Attempting automatic RPC configuration to bitcoind
Automatically obtained bitcoind's RPC credentials
2022-11-12 15:29:28.364 [INF] LTND: Version: 0.15.3-beta commit=v0.15.3-beta, build=production, logging=default, debuglevel=info
2022-11-12 15:29:28.364 [INF] LTND: Active chain: Bitcoin (network=testnet)
2022-11-12 15:29:28.365 [INF] RPCS: RPC server listening on 127.0.0.1:10009
2022-11-12 15:29:28.367 [INF] RPCS: gRPC proxy started at 0.0.0.0:8080
...

// Ryan creates wallet
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli create
Input wallet password: 
Confirm password: 

Do you have an existing cipher seed mnemonic or extended master root key you want to use?
Enter 'y' to use an existing cipher seed mnemonic, 'x' to use an extended master root key 
or 'n' to create a new seed (Enter y/x/n): n
...

// Bob starts his lnd node: 
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lnd --configfile=lnd.conf
Attempting automatic RPC configuration to bitcoind
Automatically obtained bitcoind's RPC credentials
2022-11-12 18:52:21.976 [INF] LTND: Version: 0.15.3-beta commit=v0.15.3-beta, build=production, logging=default, debuglevel=info
2022-11-12 18:52:21.976 [INF] LTND: Active chain: Bitcoin (network=testnet)
2022-11-12 18:52:21.977 [INF] RPCS: RPC server listening on 127.0.0.1:10010
2022-11-12 18:52:21.980 [INF] RPCS: gRPC proxy started at 0.0.0.0:8081
...

// Bob creates wallet
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli create
Input wallet password: 
Confirm password: 

Do you have an existing cipher seed mnemonic or extended master root key you want to use?
Enter 'y' to use an existing cipher seed mnemonic, 'x' to use an extended master root key 
or 'n' to create a new seed (Enter y/x/n): n
...

// Ryan creates new send address and address funded via Bitcoin core:
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli newaddress p2wkh
{
    "address": "tb1q2lqehz7676l2cys0aeennjxkv5wa2wtg4st708"
}

// Bob creates new send address and address funded via Bitcoin core:
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli newaddress p2wkh
{
    "address": "tb1qpu06hsmnhue7n5px2g2w7sjx7jsv4lj7nyln67"
}

// Get info of Bob's node (identity_pubkey) to add to Ryan's wallet to connect and create channel
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli getinfo
{
    "version": "0.15.3-beta commit=v0.15.3-beta",
    "commit_hash": "b4e7131bdb47531ad2f00ce345ddcdb58935bba5",
    "identity_pubkey": "023fe826962aa3e1108a50a64c1b4fe62ec821174f8b080add2446cf480ddfdfa3",
    "alias": "bob",
    "color": "#3399ff",
    "num_pending_channels": 0,
    "num_active_channels": 0,
    "num_inactive_channels": 0,
...

// Ryan connect with Bob
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli connect 023fe826962aa3e1108a50a64c1b4fe62ec821174f8b080add2446cf480ddfdfa3@localhost:9737
{

}

// Ryan start channel with Bob
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli openchannel --node_key=023fe826962aa3e1108a50a64c1b4fe62ec821174f8b080add2446cf480ddfdfa3 --local_amt=250000
{
	"funding_txid": "d9fa96e7eedee54fa3ed53bb631beb826aaf743a66b2238805125591562badc8"
}

// Bob checks and sees remote balance on Ryan's end
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli channelbalance
{
    "balance": "0",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "249056",
        "msat": "249056000"
    }
}

// Ryan checks and sees remote balance pending
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli channelbalance
{
    "balance": "0",
    "pending_open_balance": "249056",
    "local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "249056",
        "msat": "249056000"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Ryan see balance is no longer pending
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli channelbalance
{
    "balance": "249056",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "249056",
        "msat": "249056000"
    },
    "remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Bob see balance is no longer pending
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli channelbalance
{
    "balance": "0",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "remote_balance": {
        "sat": "249056",
        "msat": "249056000"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Bob creates invoice 
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli addinvoice --amt=50000
{
    "r_hash": "5eb3d3ab9cd01687a44ab8eb2558265a8183086a34533a6d40a769467627ccbd",
    "payment_request": "lntb500u1p3hqnk3pp5t6ea82uu6qtg0fz2hr4j2kpxt2qcxzr2x3fn5m2q5a55va38ej7sdqqcqzpgxqyz5vqsp50l3ee3szqgr2l7cwc3asdea7yprsxdh3y05kl0rl62350xash8jq9qyyssqtdg2qyz7k4q2s82v4sv2y9mr89yfmerrkqfgg540mt9e7g5wm9dh0syv39l62hl43stdmq29z9v5ln807ttcjscwchspkyq3rx5zp4spfcq86f",
    "add_index": "1",
    "payment_addr": "7fe39cc6020206affb0ec47b06e7be20470336f123e96fbc7fd2a3479bb0b9e4"
}

// Ryan pays invoice
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli sendpayment --pay_req=lntb500u1p3hqnk3pp5t6ea82uu6qtg0fz2hr4j2kpxt2qcxzr2x3fn5m2q5a55va38ej7sdqqcqzpgxqyz5vqsp50l3ee3szqgr2l7cwc3asdea7yprsxdh3y05kl0rl62350xash8jq9qyyssqtdg2qyz7k4q2s82v4sv2y9mr89yfmerrkqfgg540mt9e7g5wm9dh0syv39l62hl43stdmq29z9v5ln807ttcjscwchspkyq3rx5zp4spfcq86f
Payment hash: 5eb3d3ab9cd01687a44ab8eb2558265a8183086a34533a6d40a769467627ccbd
Description: 
Amount (in satoshis): 50000
Fee limit (in satoshis): 2500
Destination: 023fe826962aa3e1108a50a64c1b4fe62ec821174f8b080add2446cf480ddfdfa3
Confirm payment (yes/no): yes
+------------+--------------+--------------+--------------+-----+----------+---------------------+-------+
| HTLC_STATE | ATTEMPT_TIME | RESOLVE_TIME | RECEIVER_AMT | FEE | TIMELOCK | CHAN_OUT            | ROUTE |
+------------+--------------+--------------+--------------+-----+----------+---------------------+-------+
| SUCCEEDED  |        0.033 |        0.180 | 50000        | 0   |  2406053 | 2645430473988177921 | bob   |
+------------+--------------+--------------+--------------+-----+----------+---------------------+-------+
Amount + fee:   50000 + 0 sat
Payment hash:   5eb3d3ab9cd01687a44ab8eb2558265a8183086a34533a6d40a769467627ccbd
Payment status: SUCCEEDED, preimage: 5b7a80575f2cdbaafc16f112db13b3f4a8ffb0ba563317bac32e6ce3453f960b

// Ryan sees payment in channel balance
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli channelbalance
{
    "balance": "199056",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "199056",
        "msat": "199056000"
    },
    "remote_balance": {
        "sat": "50000",
        "msat": "50000000"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Bob sees payment in channel balance
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli channelbalance
{
    "balance": "50000",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "50000",
        "msat": "50000000"
    },
    "remote_balance": {
        "sat": "199056",
        "msat": "199056000"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Ryan creates payment request back to Bob
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli addinvoice --amt=20000
{
    "r_hash": "b490dbb1fd56447dc7ccc5b32c990826dfbf9f07bf5d3e5e517d6f683abef40c",
    "payment_request": "lntb200u1p3hq5z3pp5kjgdhv0a2ez8m37vckejexggym0ml8c8hawnuhj304hksw477sxqdqqcqzpgxqyz5vqsp5ymakk6ljtqkt69a06z25heg5shqkxfu0v7d3jlk4z00wju7hljns9qyyssqr4y3qkm7zznrp757v5ejvq08r4mw4psyg54nq2mxp7wkly3w6syy7kwpq5fzcsfe0663wgewlyycnvf295lkvuvrjdhd46vmkvwpn3cp8hwxmk",
    "add_index": "1",
    "payment_addr": "26fb6b6bf2582cbd17afd0954be51485c163278f679b197ed513dee973d7fca7"
}

// Bob pays payment request
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli sendpayment --pay_req=lntb200u1p3hq5z3pp5kjgdhv0a2ez8m37vckejexggym0ml8c8hawnuhj304hksw477sxqdqqcqzpgxqyz5vqsp5ymakk6ljtqkt69a06z25heg5shqkxfu0v7d3jlk4z00wju7hljns9qyyssqr4y3qkm7zznrp757v5ejvq08r4mw4psyg54nq2mxp7wkly3w6syy7kwpq5fzcsfe0663wgewlyycnvf295lkvuvrjdhd46vmkvwpn3cp8hwxmk
Payment hash: b490dbb1fd56447dc7ccc5b32c990826dfbf9f07bf5d3e5e517d6f683abef40c
Description: 
Amount (in satoshis): 20000
Fee limit (in satoshis): 1000
Destination: 02e5f54bab50dd5be5a16edc9debe36a9c56d0c7a8887bdb672b565f129db9be1d
Confirm payment (yes/no): yes
+------------+--------------+--------------+--------------+-----+----------+---------------------+-------+
| HTLC_STATE | ATTEMPT_TIME | RESOLVE_TIME | RECEIVER_AMT | FEE | TIMELOCK | CHAN_OUT            | ROUTE |
+------------+--------------+--------------+--------------+-----+----------+---------------------+-------+
| SUCCEEDED  |        0.026 |        0.174 | 20000        | 0   |  2406054 | 2645430473988177921 | ryan  |
+------------+--------------+--------------+--------------+-----+----------+---------------------+-------+
Amount + fee:   20000 + 0 sat
Payment hash:   b490dbb1fd56447dc7ccc5b32c990826dfbf9f07bf5d3e5e517d6f683abef40c
Payment status: SUCCEEDED, preimage: f200403a57fff35b8563e718a83341218191c5fc4f58cad1961113320cff4d33

// Ryan sees change in balance
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli channelbalance
{
    "balance": "219056",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "219056",
        "msat": "219056000"
    },
    "remote_balance": {
        "sat": "30000",
        "msat": "30000000"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Bob sees change in balance
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli channelbalance
{
    "balance": "30000",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "30000",
        "msat": "30000000"
    },
    "remote_balance": {
        "sat": "219056",
        "msat": "219056000"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Ryan closes channel
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli closeallchannels
{
	"remote_pub_key": "023fe826962aa3e1108a50a64c1b4fe62ec821174f8b080add2446cf480ddfdfa3",
	"channel_point": "d9fa96e7eedee54fa3ed53bb631beb826aaf743a66b2238805125591562badc8:1",
	"closing_txid": "19d0278a3f2e12d9789fe59eec1fc9ddae9e450316b3b0de473f79e10d0d713f",
	"error": ""
}

// Bob sees channel is closed
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli channelbalance
{
    "balance": "0",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Bob sees that he has a net 30,000 satoshis from the transactions in the channel (received 50,000 then sent 20,000)
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/bob$ ./lcli walletbalance
{
    "total_balance": "30000",
    "confirmed_balance": "0",
    "unconfirmed_balance": "30000",
    "locked_balance": "0",
    "reserved_balance_anchor_chan": "10000",
    "account_balance": {
        "default": {
            "confirmed_balance": "0",
            "unconfirmed_balance": "30000"
        }
    }
}

// Ryan sees the channel balance reflects the funding amount minus the 30,000 satoshis to Bob
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli walletbalance
{
    "total_balance": "269639",
    "confirmed_balance": "49834",
    "unconfirmed_balance": "219805",
    "locked_balance": "0",
    "reserved_balance_anchor_chan": "10000",
    "account_balance": {
        "default": {
            "confirmed_balance": "49834",
            "unconfirmed_balance": "219805"
        }
    }
}

// Ryan sees the channel is closed
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo-testnet/ryan$ ./lcli channelbalance
{
    "balance": "0",
    "pending_open_balance": "0",
    "local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "unsettled_remote_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_local_balance": {
        "sat": "0",
        "msat": "0"
    },
    "pending_open_remote_balance": {
        "sat": "0",
        "msat": "0"
    }
}

// Bob sends coins from lightning node back to on-chain once funds are confirmed
ryan@ryan-ThinkPad-T470p:~/ut/bitcoin/bergsy-bitcoin/code/lnd-demo/bob$ ./lcli sendcoins bcrt1qmfy0laf7x6nv502glx4w97rcqrrezay3ymcv3p 10000
TODO: FILL IN

```