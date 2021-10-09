print("client ")
import os 
import logging
absolute_path=os.path.dirname(os.path.abspath(__file__))
# logging.basicConfig(filename=os.environ.get("LOGGER_PATH", absolute_path+"../../../logs/diem.log"),
#                     encoding='utf-8', 
#                     level=os.environ.get("LOGGER_LEVEL",logging.DEBUG),
#                     )

# logging.info("Current Build Path : "+absolute_path)
print("Current build path : "+absolute_path)
os.system('python -m da '+absolute_path+'/*.da')
