# DiemBFT
- Implementation of DiemBFT : State Machine Replication in Diem Bloackchain as mentioned in 
https://developers.diem.com/papers/diem-consensus-state-machine-replication-in-the-diem-blockchain/2021-08-17.pdf .
We have used **DistAlgo** high level language for implementation. DistAlgo's respository can be found on
https://github.com/DistAlgo/distalgo and the home page for the same can be found on http://distalgo.cs.stonybrook.edu/.

## 1. Platform
### Operating system
- Our Implmentation of DiemBFT has been tested on GNU/Linux only.

### Python
- DiemBFT required python version 3.7.11 which can be obtained from http://www.python.org.
3.7.11 is mostly recommended since the latest version(Pre-Release) of DistAlgo runs smoothly on this version.
Please note that it is mandatory to make sure that the default Python used by the system is python 3.7.11. 
- This can be checked easily with the help of ``` python --version ``` command. It is highly 
recommended to use Anaconda(conda) virtual environment for managing different versions of python in 
a system. The steps for Anaconda installation is provided in Manual.

## 2. Workload generation
- In testdiem.da, we have included a dictionary which consists of the Workload generations parameters as mentioned in the example below. More details can be found in the test setup section in report. 
    ```
    {
      'Name' : "Normal Replicas", 
      'faultyReplicas': 1,    # number of replicas which can go faulty
      'timeoutDelta'  : 2500, # Used by Pacemaker for timeout in milliseconds
      'clients'       : 1,    # Number of Client processes
      'requests'      : 10,   # Total Number of Requests by each client
      'clientTimeout' : 5,    # ClientTimeout in Seconds
      'testcase':{
        "type":"normal",
        "specialArguments": [] # Special Arguments included for different configurations
      }
    ```

## 3. Timeouts
- For get_round_timer in Pacemaker, We use the formula 4* **delta** where delta is passed as the timeout value from setup.

## 4. Bugs and Limitations
- Limitation 1 - Currently due to design of mempool if there is a timeout and client resends a transaction. Mempool considers it as a duplicate. Hence, during timeouts the blocks which were pending or getting processed are lost.
    - This can be worked around by not keeping a state for transactions which are currently processing in diem chain. Instead, we can simply remove them from other replica queue's when a proposal message is sent. 
- Limitation 2 - Use of dummy blocks for chain termination. More details in Chain Termination under Implementation section in report.

## 5. Main files
- **DiemBFT/src/diem_replica.da :** Replica code . It mainly contains the Main fucntion as mentioned in the Pseudocode
- **DiemBFT/src/testdiem.da :** The Driver code that spawns the Clients and Replicas as per the configuaration. This is the **Run** class as mentioned in the phase doc 
- **DiemBFT/src/client.da :** The client code which send and receives commans from the replica's
- **DiemBFT/src/leader_election.py :** The leader election code.
- **DiemBFT/src/Pacemaker.py :** The pacemaker code.
- **DiemBFT/src/Ledger.py :** The Ledger code.
- **DiemBFT/src/BlockTree.py :** Code for VoteInfo, LedgerCommitInfo, QC, VoteMsg, Block, PendingBlockTree, BlockTree. (included in one to avoid circular dependency)
- **DiemBFT/src/mempool.py :** Code for mempool.


## 6. Code Size
- Cloc report in codesize.txt
- Total code lines is 2316
- Non essential code (tests, helper methods etc) is 353
## 7. Language Feature usage
- **List Comprehensions =** Total 2 : 1 in client.da and 1 in diem_replica.da
- **Dictionary Comprehensions =** 0
- **set comprehensions =** 0
- **aggregations  =** 0
- **quantifications =** 1 Quantification(some) in  diem_replica.da 
- **await statements =** Total 5: 2 each in diem_replica.da (not counting its variants), 2 in client.da and 1 in testdiem.da respectively
- **receive handlers =** Total 5 : 4 in diem_replica.da and 1 in client.da

## 8. Contributions
* Raj Patel (114363611)
    - Test Setup and event loop
    - Main Procedure
    - PaceMaker
    - LeaderElection
    - Clients
    - Synchronization
    - Mempool
    - 3 TestCases
    - Bug fixes, all module integration and debugging
    - Test report and documentation
* Prince Kumar Maurya (114354075)
    - Ledger
    - BlockTree
    - Logging
    - 2 Test Case
    - Debugging
    - Crytography
    - Block Sync
* Vishal Singh (114708875)
    - PaceMaker
    - Safety
    - Signature Verification
    - 1 Test Case
    - Readme and Manual

## 9. Other
Guide to TAs 
1. report.pdf contains the test case report with detailed documentation of implementation
2. pseudo_code.pdf contains the pseudo_code requested. 
3. src folder contains all the code files