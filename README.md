# DiemBFT
Implementation of DiemBFT : State Machine Replication in Diem Bloackchain as mentioned in 
https://developers.diem.com/papers/diem-consensus-state-machine-replication-in-the-diem-blockchain/2021-08-17.pdf .
We have used **DistAlgo** high level language for implementation. DistAlgo's respository can be found on
https://github.com/DistAlgo/distalgo and the home page for the same can be found on http://distalgo.cs.stonybrook.edu/.

# 1. Platform
## Operating system
DiemBFT has been tested on GNU/Linux only.

## Python
DiemBFT required python version 3.7.11 which can be obtained from http://www.python.org.
3.7.11 is mostly recommended since the latest version(Pre-Release) of DistAlgo runs smoothly on this version.
Please note that it is mandatory to make sure that the default Python used by the system is python 3.7.11. 
This can be checked easily with the help of ``` python --version ``` command. It is highly 
recommended to use Anaconda(conda) virtual environment for managing different versions of python in 
a system. The steps for Anaconda installation is provided in Setup below

## 2. Workload generation

## 3. Timeouts
- For get_round_timer in Pacemaker, We use the Hardcoded delta value in the formula 4* *delta* as timeout value

## 4. Bugs and Limitations

## 5. Main files
- DiemBFT/src/diem_replica.da : Replica code . It mainly contains the Main fucntion as mentioned in the Pseudocode
- DiemBFT/src/testdiem.da : The Driver code that spawns the Clients and Replicas as per the configuaration. This is the **Run** class as mentioned in the phase doc 
- DiemBFT/src/client.da : The client code which send and receives commans from the replica's

## 6. Code Size

## 7. Language Feature usage
- List Comprehensions = Todo
- Dictionary Comprehensions = Todo
- set comprehensions = 0
- aggregations  = 0
- quantifications = 1 Quantification(some) in  diem_replica.da 
- await statements = 1 in diem_replica.da
- receive handlers = Total 5 : 4 in diem_replica.da and 1 in client.da

## 8. Contributions

## 9. Other