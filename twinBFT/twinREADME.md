# DiemBFT
- Implementation of twinBFT : Twins: Making BFT Systems Robust as mentioned in 
https://sonnino.com/papers/twins.pdf.

We have used **DistAlgo** high level language for implementation. DistAlgo's respository can be found on
https://github.com/DistAlgo/distalgo and the home page for the same can be found on http://distalgo.cs.stonybrook.edu/.

## 1. Platform
### Operating system
- Our Implmentation of twinBFT has been tested on GNU/Linux only.

### Python
- DiemBFT required python version 3.7.11 which can be obtained from http://www.python.org.
3.7.11 is mostly recommended since the latest version(Pre-Release) of DistAlgo runs smoothly on this version.
Please note that it is mandatory to make sure that the default Python used by the system is python 3.7.11. 
- This can be checked easily with the help of ``` python --version ``` command. It is highly 
recommended to use Anaconda(conda) virtual environment for managing different versions of python in 
a system. The steps for Anaconda installation is provided in Manual.

## 2. Scenario generation
- We use scenario_generator.py file to generate scenarios. The scenario generation logic is mentioned in the **phase_3/pseudocode/scenario_executor** file. A sample scenario and its explanation is mentioned in the twinBFT Report

## 3. Bugs and Limitations
- 

## 4. Main files
- **twinBFT/scenario_generator.py	 :** ScenarioGenerator code
- **twinBFT/Loyal_Byzantine_Generals_phase_2/src/scenario_executor.da :** The Driver code that runs  spawns teh clients and validtors as per the configuration/scenario passed. \
- **twinBFT/Loyal_Byzantine_Generals_phase_2/src/network_playground.da  :** The code of NetworkPlayground which acts as a NetoworkTunnel.
- **twinBFT/Loyal_Byzantine_Generals_phase_2/src/leader_election.da :** This the file that overrides the leader election module in DiemBFT. The leader for each round is taken from the configuration file


## 5. Code Size
- Cloc report in codesize.txt
- Total code lines is 4048
- Non essential code (tests, helper methods etc) is 753

## 7. Language Feature usage

- **List Comprehensions =** 0
- **Dictionary Comprehensions =** 0
- **set comprehensions =** 0
- **aggregations  =** 0
- **quantifications =** 0 
- **await statements =** Total 2: 1 each in network_playground.da and scenario_executor.da
- **receive handlers =** Total 3 : 3 in network_playground.da

## 8. Contributions

All 3 members contributed equally to the project. Below are some of the notable contributions by each team member
* Raj Patel (114363611)
    - SyncUP
    - Client Deduplication
* Prince Kumar Maurya (114354075)
    - ScenarioExecutor
	- Network Playground
* Vishal Singh (114708875)
    - HashValidation
    - ScenarioGenerator
    - Readme and Manual

## 9. Other
Guide to TAs 
1. twinBFT Report.pdf contains the test case report with detailed documentation of implementation
2. pseudocod folder contains the pseudo_code requested for each modules. 
3. twinBFT/Loyal_Byzantine_Generals_phase_2/src folder contains all the code files