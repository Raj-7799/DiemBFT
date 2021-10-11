import os 
absolute_path=os.path.dirname(os.path.abspath(__file__))
os.system('python -m da '+absolute_path+'/*.da')