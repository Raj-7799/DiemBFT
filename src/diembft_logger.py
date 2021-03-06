import logging
import sys
from logging.handlers import TimedRotatingFileHandler
LOG_FILE = "diem.log"

def get_console_handler(FORMATTER):
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler

def get_file_handler(FORMATTER):
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler


   
def get_logger(logger_name,replicaID=-1):
   logger = logging.getLogger(logger_name)
   FORMATTER = logging.Formatter("%(asctime)s — %(lineno)d — %(name)s — %(funcName)20s() — %(levelname)s — [ReplicaID-{}] %(message)s".format(replicaID))

   #logger.setLevel(logging.INFO) # better to have too much log than not enough
   logger.addHandler(get_console_handler(FORMATTER))
   logger.addHandler(get_file_handler(FORMATTER))
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger