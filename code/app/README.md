## AirBNB Bitcoin
1. Unique property/host ID
2. Calendar shows availability - queries blockchain for info
3. Uses unique identifier + user's wallet to generate transaction for given dates
4. 2 of 2 multisig with renter and property owner and timelock? OP_RETURN?

Options:
1. Renter connects wallet, sends funds to host/owner, output(s) are in a timelock contract until booked date. OP_RETURN holds date range.
    - Host enters their address into tool first time to create host account. Then add photos of property associated with account.
    - Somehow hide notes/key/passcode behind a transaction back to the renter. Would be timelocked to day of renting. Colored coin? Other return using renter's pubkey? --> Could just have it be a transaction with OP_RETURN as long as BTC address isn't linked to physical home address.
    - How to handle cancelations? Smart contract with 2 of 3 to return funds if requested?
    - Static wallet address for host/home?
2. Renter sends relative timelock transaction to start date of stay. Output timelock at end of stay.
