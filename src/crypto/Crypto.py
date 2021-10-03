import nacl.utils
from nacl.public import PrivateKey, SealedBox,Box
import glob


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
        self._key_pairs[idx]=(public_key,key)
        self._public_keys[idx]=key.public_key
        
    def write_config(self):
        
        for dic_key in self._key_pairs.keys():
            with open("../../conf/diem_key_"+str(dic_key)+"_.sec.conf","w") as file:
                entry = ["private_key="+ str(self._key_pairs[dic_key][1]),"\npublic_key="+ str(self._key_pairs[dic_key][0])]
                file.writelines(entry)                

    def read_config(self):
        #pass 
        conf_files= [f for f in glob.glob("diem_key_*.sec.conf")]

        for file in conf_files:
            idx =  file.split['_']
            with open("diem_key_"+idx+".sec.conf","r") as file:
                entry = file.readLines(2)
                
    def encrypt(self,msg,from_idx,to_idx):               
        sender_box = Box(self._get_key_pair(from_idx)[1], self._get_public_keys(to_idx))
        return sender_box.encrypt(str.encode(msg))     
    
    def decrypt(self,msg,from_idx,to_idx):
        receiver_box = Box(self._get_key_pair(to_idx)[1],self._get_public_keys(from_idx))
        return receiver_box.decrypt(msg).decode('utf-8')


        
x = GenerateKey(5)
# x.write_config()
# print(x.key_pairs)
enc_msg=(x.encrypt("test",from_idx=0,to_idx=1))
dcyp_mes=x.decrypt(enc_msg,to_idx=1,from_idx=0)
print(dcyp_mes)
