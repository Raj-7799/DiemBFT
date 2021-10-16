# DiemBFT
Implementation of DiemBFTv4: State Machine Replication in Diem Bloackchain as mentioned in 
[a link](https://developers.diem.com/papers/diem-consensus-state-machine-replication-in-the-diem-blockchain/2021-08-17.pdf


## Setup 
- Install conda 
    Conda is an open source package management system and environment management system that runs on Windows, macOS and Linux. Conda quickly installs, runs and updates packages and their dependencies. Conda easily creates, saves, loads and switches between environments on your local computer. It was created for Python programs, but it can package and distribute software for any language.
- Clone the repo
    git clone git@github.com:Raj-7799/DiemBFT.git
- cd DIEMBFT

- Create Conda Environment 
    ``` conda create --name <env> --file requirement.txt ```
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