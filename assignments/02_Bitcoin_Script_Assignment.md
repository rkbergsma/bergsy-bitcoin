# Assignment 02 - Bitcoin Script

The purpose of this assignment is to demonstrate that you can construct a valid Bitcoin script, which validates to *true* (i.e is spendable).

## Requirements

* A document within your repository, which shows the contents of your Bitcoin script, and the valid output.

* A valid Bitcoin Script, which evaluates to *true* on [https://ide.scriptwiz.app](https://ide.scriptwiz.app).

## Resources

**Scriptwiz Bitcoin Script IDE**  
https://ide.scriptwiz.app

## Solution
The code for the Bitcoin Script resides [here](https://github.com/rkbergsma/bergsy-bitcoin/blob/master/script/rock-paper-scissors.txt) and shows how you can play a simple game of rock, paper, scissors in Bitcoin script. The script will return true if the first player beats the second player, otherwise it will be false. 

The script makes use of several OP codes:
`OP_2DUP`: to duplicate the top two items of the stack. This also enforces there to be at least 2 items on the stack.  
`OP_EQUAL`: To check that the two top items of the stack are equal.  
`OF_IF`: To check if a condition (such as `OP_EQUAL`) is true or false. Must result in either a 1 or 0.  
`OP_ELSE`: Control logic to accompany `OP_IF`.  
`OP_OVER`: To copy the second stack element to the top of the stack.
`OP_DROP`: To remove items from the stack.  
`OP_1`: Put the number 1 on the stack (also can allow the script to return true if it is the only thing on the stack).  

I included screenshots in the [script directory](https://github.com/rkbergsma/bergsy-bitcoin/blob/master/script/) of the three winning scenarios, where rock beats scissors, paper beats rock, as well as scissors beats paper. I also included one failing scenario, but any other scenario will fail and not evaluate to true. As a note, this script would be refactored if ever used in an actual transaction, since it uses many OP_CODES and would therefore be expensive to perform a relatively simple task.