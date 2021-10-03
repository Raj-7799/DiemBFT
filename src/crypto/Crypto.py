import nacl.utils
from nacl.public import PrivateKey, SealedBox


class GenerateKey():


    def __init__(self,count):
        self.count=count
        self._key_pairs=dict()
        self._public_keys=dict()    
        for i in range(count):
            self.generate(i)

    @property
    def key_pairs(self,idx):
        if idx==-1:
            return self._key_pairs
        return self._key_pairs[idx]

    @property
    def public_keys(self,idx):
        if idx==-1:
            return self._public_keys
        return self._public_keys[idx]

    @key_pairs.setter
    def key_pairs(self,key_pair,idx):
        self._public_keys[idx]=key_pair[0]
        self._key_pairs[idx]=(key_pair)

    @key_pairs.deleter
    def key_pairs(self,idx):
        if idx == -1:
            del self._public_keys
            del self._key_pairs
        else: 
            del self._public_keys[idx]
            del self._key_pairs[idx]


    def generate(self,idx):
        key = PrivateKey.generate()
        public_key = (key.public_key)._public_key.hex()
        private_key = key._private_key.hex()
        self._key_pairs[idx]=(public_key,private_key)
        
    def write_config(self):
        
        for dic_key in self._key_pairs.keys():
            with open("../conf/diem_key_"+str(dic_key)+".sec.conf","w") as file:
                entry = ["private_key="+ str(self._key_pairs[dic_key][1]),"\npublic_key="+ str(self._key_pairs[dic_key][0])]
                file.writelines(entry)                

    def read_config(self):
        #pass 
        

# x = GenerateKey(5)
# x.write_config()