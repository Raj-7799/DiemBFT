
import Quorum as qc
import nacl.encoding
import nacl.hash
HASHER = nacl.hash.sha256

def max_round_qc(current_qc,high_qc):
    qc_round =  current_qc.vote_info.round
    print(type(high_qc))
    high_qc_round =  high_qc.vote_info.round
    if qc_round >  high_qc_round:
        return current_qc
    else:
        return high_qc


def hash(object):
    digest = HASHER(bytes(object,'utf-8'), encoder=nacl.encoding.HexEncoder)
    return digest

def serialize(object, schema):
    return schema.dumps(object)

def deserialize(json, schema):
    return schema.loads(json)

    

