## 1. Setup 

### Installation via requirements.txt

- Step 1 - **Install conda** :: Install Linux script for conda from https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh and run the command ```bash Anaconda-latest-Linux-x86_64.sh``` to install. Follow https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart to refer for step-by-step installation
- Step 2 - **Clone the repo** :: ``` git clone git@github.com:Raj-7799/DiemBFT.git ```
- Step 3 - **Enter src folder** :: ``` cd DIEMBFT/src ```
- Step 4  - **Create Conda Environment** :: ``` conda create --name <env> --file requirement.txt ```
### Alternate way is to install dependencies is to manuall run the following commands
``` bash
conda create --name diem python=3.6
conda activate diem
pip install --pre pyDistAlgo
pip install pickle
pip install pynacl
pip install plyvel
pip install tabulate
```
## 2. Running Diem 
### Command to run the driver code from the source folder
- ``` python -m da --message-buffer-size 102400 testdiem.da &> out.log  ```
