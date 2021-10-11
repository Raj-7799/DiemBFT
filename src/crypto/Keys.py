from nacl.public import PrivateKey, PublicKey,SealedBox,Box
from nacl.signing import SigningKey,VerifyKey
from nacl.exceptions import BadSignatureError
from nacl.encoding import HexEncoder
import os



absolute_path=os.path.dirname(os.path.abspath(__file__))
CONF_FILE_PATH=absolute_path+"/../../conf/"

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

        with open(CONF_FILE_PATH+self.config_file,"r") as file:
            entry = file.read().splitlines() 
            #self._private_key=PrivateKey(bytes.fromhex(entry[0].split("=")[1]))       
            #self._public_key=PublicKey(bytes.fromhex(entry[1].split("=")[1]))
            
          
            private_key_from_file=bytes(entry[0].split("=")[1],'utf-8')
            public_key_from_file=bytes(entry[1].split("=")[1],'utf-8')
            private_key=HexEncoder.decode(private_key_from_file)
            self._private_key=(SigningKey)(private_key)
            self._public_key=VerifyKey(public_key_from_file,encoder=HexEncoder)
            
        
        with open(CONF_FILE_PATH+self._public_key_file,"r") as file:
            entries=file.read().splitlines() 
            for entry in entries:
                #self._public_keys.append(PublicKey(bytes.fromhex(entry.split("=")[1])))
                public_key_from_file=bytes(entry.split("=")[1],'utf-8')
                public_key=VerifyKey(public_key_from_file,encoder=HexEncoder)
                self._public_keys.append(public_key)

            
    def encrypt(self,msg,to_idx):         
        priv_key = self.private_key
        pub_key = self.public_keys[to_idx]
        #Box needs private key and Public key object
        sender_box = Box(priv_key,pub_key)
        return sender_box.encrypt(str.encode(msg))     
    
    def decrypt(self,msg,from_idx):
        priv_key = self.private_key
        pub_key = self.public_keys[from_idx]
        #Box needs private key and Public key object
        receiver_box = Box(priv_key,pub_key)
        return receiver_box.decrypt(msg).decode('utf-8')

    ##Uses only receivers public key, which only reciever can decrypt using its private key 
    def encrypt_no_trace(self,msg,reciever_id):
        msg = bytes(msg,"utf-8")
        receiver_public_key = self.public_keys[reciever_id]
        seal_box=SealedBox(receiver_public_key) #
        return seal_box.encrypt(msg)

    def decrypt_no_trace(self,enc_msg):
        unseal_box=SealedBox(self.private_key)
        return unseal_box.decrypt(enc_msg).decode("utf-8")


    ## Use the below method for siging the message 
    ## Reference : https://pynacl.readthedocs.io/en/latest/signing/#id1
    def sign_message(self,msg):        
        msg=bytes(msg,"utf-8")        
        signed_hex = self._private_key.sign(msg,encoder=HexEncoder)
        verify_key = self._public_key
        verify_key_hex = verify_key.encode(encoder=HexEncoder)        
        return [signed_hex,verify_key_hex]



    def verify_message(self,signed_msg):
        signed_hex, verify_key_hex=signed_msg
        signature_bytes = HexEncoder.decode(signed_hex.signature)
        verify_key = VerifyKey(verify_key_hex,encoder=HexEncoder)
        try:
            return verify_key.verify(signed_hex.message,signature_bytes,encoder=HexEncoder)
        except BadSignatureError:
            return None

    @property
    def getKeyValuePair(self):
        return {
            "public" : self.public_key(),
            "private" : self.private_key()
        }

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

# result =k.sign_message("test")
# print(k0.verify_message(result))

# enc_msg_no_trace= k.encrypt_no_trace("tmp1",0)
# print(k0.decrypt_no_trace(enc_msg_no_trace))

# k=Keys(1)
# print(k.public_key)
# result=k.sign_message("tmp")
# print(result)


# k0=Keys(0) 
# print(k0.verify_message(result))