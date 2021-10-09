import os 
absolute_path=os.path.dirname(os.path.abspath(__file__))
print("Current build path : "+absolute_path)
os.system('python -m da '+absolute_path+'/*.da')