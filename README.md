# DiemBFT
<<<<<<< HEAD
Implementation of DiemBFTv4: State Machine Replication in Diem Bloackchain as mentioned in 
[a link](https://developers.diem.com/papers/diem-consensus-state-machine-replication-in-the-diem-blockchain/2021-08-17.pdf
=======
Implementation of DiemBFT : State Machine Replication in Diem Bloackchain as mentioned in 
https://developers.diem.com/papers/diem-consensus-state-machine-replication-in-the-diem-blockchain/2021-08-17.pdf .
We have used **DistAlgo** high level language for implementation. DistAlgo's respository can be found on
https://github.com/DistAlgo/distalgo and the home page for the same can be found on http://distalgo.cs.stonybrook.edu/.
>>>>>>> d97c3f09c0f53359716036cf16afc2d37c72ffc8

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

## 2. Setup 

### Installation via requirements.txt

- Step 1 - **Install conda** :: Install Linux script for conda from https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh and Run the command ```bash Anaconda-latest-Linux-x86_64.sh``` to install. Follow https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart to refer for step-by-step installation
- Step 2 - **Clone the repo** :: ``` git clone git@github.com:Raj-7799/DiemBFT.git ```
- Step 3 - **Enter src folder** :: ``` cd DIEMBFT/src ```
- Step 4  - **Create Conda Environment** :: ``` conda create --name <env> --file requirement.txt ```
### Alternate way is to install dependencies is to manuall run the following commands
``` bash
conda create --name diem python=3.7
conda activate diem
pip install --pre pyDistAlgo
pip install pickle
pip install pynacl
pip install plyvel
pip install tabulate
```
## 3. Running Diem 
### Command to run the driver code from the source folder
- ``` python -m da --message-buffer-size 1024000 testdiem.da &> out.log  ```

## 4. Workload generation

## 5. Timeouts
- For get_round_timer in Pacemaker, We use the Hardcoded delta value in the formula 4* *delta* as timeout value

## 6. Bugs and Limitations

## 7. Main files
- DiemBFT/src/diem_replica.da : Replica code . It mainly contains the Main fucntion as mentioned in the Pseudocode
- DiemBFT/src/testdiem.da : The Driver code that spawns the Clients and Replicas as per the configuaration. This is the **Run** class as mentioned in the phase doc 
- DiemBFT/src/client.da : The client code which send and receives commans from the replica's

## 8. Code Size

## 9. Language Feature usage
- List Comprehensions
- Dictionary Comprehensions
- set comprehensions
- aggregations
- quantifications
- await statements
- receive handlers

## 10. Contributions

## 11. Other

