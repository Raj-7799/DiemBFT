# DiemBFT
Implementation of DiemBFT


## Setup 
- Install conda 
- Clone the repo
- cd DIEMBFT
- run ``` conda create --name <env> --file requirement.txt ```
### Alternate way is to manuall run the following pip
- run  ``` conda create --name diem python=3.6  ```
- ``` conda activate diem ```
- ``` pip install pyDistAlgo ```
- ``` pip install pynacl ```
- ``` pip install bz2file ```
- ``` pip install plyvel ```

### Command to run code
- ``` python -m da --message-buffer-size 102400 testdiem.da &> out.log  ```