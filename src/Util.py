
import Quorum as qc
import nacl.encoding
import nacl.hash
from nacl.public import PrivateKey, PublicKey,SealedBox,Box
from nacl.signing import SigningKey,VerifyKey
from nacl.exceptions import BadSignatureError
from nacl.encoding import HexEncoder
from VoteInfo import VoteInfo as vi
from LedgerCommitInfo import LedgerCommitInfo as lci
from Block import Block as block

import pickle


def max_round_qc(current_qc,high_qc):
    qc_round =  current_qc.vote_info.round
    high_qc_round =  high_qc.vote_info.round
    if qc_round >  high_qc_round:
        return current_qc
    else:
        return high_qc

def hash(object):
    hasher = nacl.hash.sha256
    digest = hasher(pickle.dumps(object), encoder=nacl.encoding.HexEncoder)
    return digest

def sign_object(obj, pvt_key, pbc_key):
    return sign_message(pickle.dumps(obj), pvt_key, pbc_key)

def sign_message(pickled_msg, pvt_key, pbc_key):    
    signed_hex = pvt_key.sign(pickled_msg ,encoder=HexEncoder)
    verify_key = pbc_key
    verify_key_hex = verify_key.encode(encoder=HexEncoder)        
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

## Creating genesis block for startup 
def create_genesis_object():
    genesis_voteInfo = vi.VoteInfo(id=0,round_no=0,parent_id=0,parent_round=0,exec_state_id=0)
    ledger_commit_info = lci.LedgerCommitInfo(commit_state_id=0,vote_info_hash=genesis_voteInfo)  
    
    genesis_qc = qc.QC(vote_info=genesis_voteInfo,ledger_commit_info=ledger_commit_info)        
    genesis_block =  block.Block(0,0,"genesis",genesis_qc)
    
    return genesis_qc , genesis_block
