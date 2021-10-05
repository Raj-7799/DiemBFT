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




# k=Keys(1)
# k0=Keys(0) 
# enc_msg=k.encrypt("tmp",0)
# dcyp_mes=k0.decrypt(enc_msg,1)
# print(dcyp_mes)
