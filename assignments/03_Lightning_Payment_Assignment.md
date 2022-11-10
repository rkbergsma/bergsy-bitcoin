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

```

### Testnet: