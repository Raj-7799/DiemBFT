import nacl.encoding
import nacl.hash
from nacl.public import PrivateKey, PublicKey,SealedBox,Box
from nacl.signing import SigningKey,VerifyKey
from nacl.exceptions import BadSignatureError
from nacl.encoding import HexEncoder
import bz2
import sys
import pickle



import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))

def max_round_qc(current_qc,high_qc):
    qc_round =  current_qc.vote_info.roundNo
    high_qc_round =  high_qc.vote_info.roundNo
    if qc_round >  high_qc_round:
        return current_qc
    else:
        return high_qc

def hash(object):
    hasher = nacl.hash.sha256
    digest = hasher(pickle.dumps(object), encoder=nacl.encoding.HexEncoder)
    return digest

def sign_object(obj, pvt_key, pbc_key):
    seralized_msg =  pickle.dumps(obj)
    return sign_message(seralized_msg, pvt_key, pbc_key)

def sign_message(pickled_msg, pvt_key, pbc_key):    
    
    print("Start Signing")
    signed_hex = pvt_key.sign(pickled_msg ,encoder=HexEncoder)
    verify_key = pbc_key
    print("Signed Successful")
    verify_key_hex = verify_key.encode(encoder=HexEncoder)
    
    print("Encoding Successful")     
    return [signed_hex,verify_key_hex]

def check_authenticity(obj, signed_msg):
    objIdentity = verify_message(signed_msg)
    return pickle.dumps(obj) == objIdentity

def verify_message(signed_msg):
    signed_hex, verify_key_hex=signed_msg
    signature_bytes = HexEncoder.decode(signed_hex.signature)
    verify_key = VerifyKey(verify_key_hex,encoder=HexEncoder)
    try:
        return verify_key.verify(signed_hex.message,signature_bytes,encoder=HexEncoder)
    except BadSignatureError:
        return None


# def sign_object(obj, pvt_key):
#     seralized_msg =  pickle.dumps(obj)
#     return sign_message(seralized_msg, pvt_key)

# def sign_message(pickled_msg, pvt_key):
#     print("Start Signing")
#     signed_hex = pvt_key.sign(pickled_msg ,encoder=HexEncoder)
#     print("Signed Successful")
#     return signed_hex

# def encode_key(key):
#     print("Start Encoding")
#     key_hex = key.encode(encoder=HexEncoder)
#     print("End Encoding")
#     return key_hex

# def check_authenticity(obj, signed_msg, pbc_key):
#     objIdentity = verify_message(signed_msg, pbc_key)
#     return pickle.dumps(obj) == objIdentity

# def verify_message(signed_msg, pbc_key):
#     signed_hex = signed_msg
#     verify_key_hex = encode_key(pbc_key)
#     signature_bytes = HexEncoder.decode(signed_hex.signature)
#     verify_key = VerifyKey(verify_key_hex,encoder=HexEncoder)
#     try:
#         return verify_key.verify(signed_hex.message,signature_bytes,encoder=HexEncoder)
#     except BadSignatureError:
#         return None
