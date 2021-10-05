import nacl.utils
from nacl.public import PrivateKey, PublicKey,SealedBox,Box
import glob
import os

from nacl import encoding
 

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
            with open("../../conf/diem_key_"+str(dic_key)+".sec.conf","w") as file:
                entry = ["private_key="+ str(self._key_pairs[dic_key][1]),"\npublic_key="+ str(self._key_pairs[dic_key][0])]
                file.writelines(entry) 

        with open("../../conf/"+public_key_file,"w") as file:
            key=[ str(i)+"="+self._public_keys[i]+"\n" for i in range(len(self._public_keys))]            
            file.writelines(key)
                    

        

    def cleanup(self):
        files=glob.glob('../../conf/*')
        print(files)
        for file in files:
            os.remove(file)


class Keys:
    def __init__(self,idx):
        self._public_keys=list()
        self._private_key=None
        self._public_key=None
        self._idx=idx
        self.config_file="diem_key_"+str(idx)+".sec.conf"
        self._public_key_file="diem_public_key.sec.conf"
        self.read_config()


    def read_config(self):

        with open("../../conf/"+self.config_file,"r") as file:
            entry = file.read().splitlines() 
            self._private_key=entry[0].split("=")[1]
       
            self._public_key=entry[1].split("=")[1]
            
        
        with open("../../conf/"+self._public_key_file,"r") as file:
            entries=file.read().splitlines() 
            for entry in entries:
                self._public_keys.append(entry.split("=")[1])

            
    def encrypt(self,msg,to_idx): 

        
        priv_key = PrivateKey(bytes.fromhex(self.private_key)) 
        pub_key = PublicKey(bytes.fromhex(self.public_keys[to_idx]))
        #Box needs private key and Public key object
        sender_box = Box(priv_key,pub_key)
        return sender_box.encrypt(str.encode(msg))     
    
    def decrypt(self,msg,from_idx):
        priv_key = PrivateKey(bytes.fromhex(self.private_key))
        pub_key = PublicKey(bytes.fromhex(self.public_keys[from_idx]))
        #Box needs private key and Public key object
        receiver_box = Box(priv_key,pub_key)
        return receiver_box.decrypt(msg).decode('utf-8')


    def sign(self,msg):
        priv_key = PrivateKey(bytes.fromhex(self.private_key))
        sign_box=SealedBox(priv_key)
        return sign_box.encrypt(msg)

    @property
    def public_key(self):
        return self._public_key

    @property
    def private_key(self):
        return self._private_key
    
    @property
    def public_keys(self):
        return self._public_keys





    
x = GenerateKey(2)
x.write_config()
k=Keys(1)
k0=Keys(0) 
enc_msg=k.encrypt("tmp",0)
dcyp_mes=k0.decrypt(enc_msg,1)
print(dcyp_mes)
