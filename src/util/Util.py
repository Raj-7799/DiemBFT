
from certificates.quorum import Quorum as qc
import nacl.encoding
import nacl.hash
HASHER = nacl.hash.sha256

def max_round_qc(current_qc,high_qc):
    qc_round =  current_qc.vote_info.round
    high_qc_round =  high_qc.vote_info.round
    if qc_round >  high_qc_round:
        return current_qc
    else:
        return high_qc_round


def hash(object):
    
    digest = HASHER(bytes(object,'utf-8'), encoder=nacl.encoding.HexEncoder)
    return digest



    

