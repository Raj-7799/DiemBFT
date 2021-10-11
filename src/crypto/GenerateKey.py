import nacl.utils
from nacl.public import PrivateKey
import glob
import os

from nacl import encoding
 
absolute_path=os.path.dirname(os.path.abspath(__file__))
CONF_FILE_PATH=absolute_path+"/../../conf/"

class GenerateKey():
    def __init__(self,count):
        self.count=count
        self._key_pairs=dict()
        self._public_keys=dict()    
        for i in range(count):
            self.generate(i)

    @property
    def key_pairs(self):
        return self._key_pairs

    @property
    def public_keys(self):        
        return self._public_keys    


    def _get_key_pair(self,idx):
        if idx in self._key_pairs.keys():
            return self._key_pairs[idx]
        return None
        
    def _get_public_keys(self,idx):
        if idx in self._public_keys.keys():
            return self._public_keys[idx]
        return None
          

    @key_pairs.deleter
    def key_pairs(self):
        del self._public_keys
        del self._key_pairs
        


    def generate(self,idx):
        key = PrivateKey.generate()
        public_key = (key.public_key)._public_key.hex()
        private_key = key._private_key.hex()
        self._key_pairs[idx]=(public_key,private_key)
        self._public_keys[idx]=public_key
        
    def write_config(self):
        self.cleanup()
        public_key_file = "diem_public_key.sec.conf"

        for dic_key in self._key_pairs.keys():
            with open(CONF_FILE_PATH+"diem_key_"+str(dic_key)+".sec.conf","w") as file:
                entry = ["private_key="+ str(self._key_pairs[dic_key][1]),"\npublic_key="+ str(self._key_pairs[dic_key][0])]
                file.writelines(entry) 

        with open(CONF_FILE_PATH+public_key_file,"w") as file:
            key=[ str(i)+"="+self._public_keys[i]+"\n" for i in range(len(self._public_keys))]            
            file.writelines(key)

        

    def cleanup(self):
        files=glob.glob(CONF_FILE_PATH+'*')
        # print(files)
        for file in files:
            os.remove(file)








    
# x = GenerateKey(2)
# x.write_config()

