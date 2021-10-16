import plyvel
import pickle

import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class Ledger:

    def __init__(self,genesis_block, replicaID):
        self.replicaID = replicaID
        self._db = plyvel.DB('/tmp/diemLedger_{}/'.format(self.replicaID), create_if_missing=True)
        self._db_speculate = plyvel.DB('/tmp/diemLedger_speculate_{}/'.format(self.replicaID), create_if_missing=True)
        self.speculate(genesis_block.id,genesis_block.id,genesis_block)
        self.commit(genesis_block.id)
        

    # apply txns speculatively
    def speculate(self,prev_block_id, block_id, txns):
        print("[Ledger][replicaID {}] Speculating for prev block {} and current block {} ".format(self.replicaID, prev_block_id, block_id))
        block_id=bytes(str(block_id),'utf-8')
        value = pickle.dumps([prev_block_id,txns])      
        self._db_speculate.put(block_id,value)


    #find the pending state for the given block id or ⊥ if not present
    def pending_state(self,bk_id):
        print("[Ledger][replicaID {}] Attempting to find pending state for block id {}".format(self.replicaID, bk_id)) 
        block_id = bytes(str(bk_id),'utf-8')     
        entry = self._db_speculate.get(block_id)
        # Check this once
        if entry is not None:
            print("[Ledger][replicaID {}] Found pending state for block id {}".format(self.replicaID, bk_id)) 
            return bk_id
        
        # TODO : fix this implementation
        if bk_id == 0 or bk_id == "0":
            print("[Ledger][replicaID {}] Received genesis block id {}".format(self.replicaID, bk_id)) 
            return bk_id
            
        return None                


    #commit the pending prefix of the given block id and prune other branches
    def commit(self,bk_id):
        block_id = bytes(str(bk_id),'utf-8')
        entry = self._db_speculate.get(block_id)
        if  entry is not None and bk_id != 0:
            print("[Ledger][replicaID {}] Commited block {}.".format(self.replicaID, bk_id)) 
            self._db.put(block_id,entry)
            # TODO : fix this
            # self._db_speculate.delete(block_id)


    #returns a committed block given its id
    def committed_block(self, bk_id):
        block_id=bytes(str(bk_id),'utf-8')
        entry = pickle.loads(self._db.get(block_id))
        if entry[1]:
            print("[Ledger][replicaID {}] Fetching commited block successfull {}.".format(self.replicaID, bk_id)) 
        else:
            print("[Ledger][replicaID {}] Failed fetching block {}.".format(self.replicaID, bk_id)) 
        
        return entry[1]


    def print_ledger(self):
        it =  self._db.iterator()
        with self._db.iterator() as it:
            for k,v  in it:
                print(k,v)