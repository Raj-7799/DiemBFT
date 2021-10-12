
import Quorum as qc
import nacl.encoding
import nacl.hash
from nacl.public import PrivateKey, PublicKey,SealedBox,Box
from nacl.signing import SigningKey,VerifyKey
from nacl.exceptions import BadSignatureError
from nacl.encoding import HexEncoder


def max_round_qc(current_qc,high_qc):
    qc_round =  current_qc.vote_info.round
    print(type(high_qc))
    high_qc_round =  high_qc.vote_info.round
    if qc_round >  high_qc_round:
        return current_qc
    else:
        return high_qc

def serialize(object, schema):
    return schema.dumps(object)

def deserialize(json, schema):
    return schema.loads(json)


def sign_message(msg, pvt_key, pbc_key):    
    msg= msg if msg is not None else " " 
    msg=bytes(msg,"utf-8")        
    signed_hex = pvt_key.sign(msg,encoder=HexEncoder)
    verify_key = pbc_key
    verify_key_hex = verify_key.encode(encoder=HexEncoder)        
    return [signed_hex,verify_key_hex]

def verify_message(signed_msg):
    signed_hex, verify_key_hex=signed_msg
    signature_bytes = HexEncoder.decode(signed_hex.signature)
    verify_key = VerifyKey(verify_key_hex,encoder=HexEncoder)
    try:
        return verify_key.verify(signed_hex.message,signature_bytes,encoder=HexEncoder)
    except BadSignatureError:
        return None

