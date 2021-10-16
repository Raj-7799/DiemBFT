# DiemBFT
Implementation of DiemBFT : State Machine Replication in Diem Bloackchain as mentioned in https://developers.diem.com/papers/diem-consensus-state-machine-replication-in-the-diem-blockchain/2021-08-17.pdf . We have used DistAlgo high level language for implementation. DistAlgo's Github respository can be found on https://github.com/DistAlgo/distalgo and the Home Page for the same can be found on http://distalgo.cs.stonybrook.edu/.


## Setup 
- Step 1 - Install conda :: Install Linux script for conda from https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh and Run the command bash Anaconda-latest-Linux-x86_64.sh to install. Follow https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart to refer for step-by-step installation
- Step 2 - Clone the repo :: git clone git@github.com:Raj-7799/DiemBFT.git
- Step 3 - cd DIEMBFT
- Step 4  - Create Conda Environment :: ``` conda create --name <env> --file requirement.txt ```
### Alternate way is to manuall run the following pip
``` bash
conda create --name diem python=3.7
conda activate diem
pip install --pre pyDistAlgo
pip install pynacl
pip install bz2file
pip install plyvel
```

### Command to run code
- ``` python -m da --message-buffer-size 1024000 testdiem.da &> out.log  ```
