import plyvel
import pickle

import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class Ledger:

    def __init__(self,genesis_block, replicaID,specluate_ledger):
        self.replicaID = replicaID
        self._db = plyvel.DB('/tmp/diemLedger_{}/'.format(self.replicaID), create_if_missing=True)
        self._db_speculate = plyvel.DB('/tmp/diemLedger_speculate_{}/'.format(self.replicaID), create_if_missing=True)
        self.specluate_ledger = specluate_ledger
        self.speculate(genesis_block.id,genesis_block.id,genesis_block)
        self.commit(genesis_block.id)
        

    # apply txns speculatively
    def speculate(self,prev_block_id, block_id, txns):
        print("[Ledger][replicaID {}] START speculate ".format(self.replicaID))
        block_id=bytes(str(block_id),'utf-8')
        value = pickle.dumps([prev_block_id,txns])      
        self._db_speculate.put(block_id,value)
        print("[Ledger][replicaID {}] END speculate ".format(self.replicaID))



    #find the pending state for the given block id or ⊥ if not present
    # def pending_state(self,bk_id):
    #     print("[Ledger][replicaID {}] START pending_state for block_id {}".format(self.replicaID, bk_id)) 
    #     block_id = bytes(str(bk_id),'utf-8')     
    #     entry = self._db_speculate.get(block_id)
    #     # Check this once
    #     if entry is not None:
    #         print("[Ledger][replicaID {}] END pending_state ".format(self.replicaID)) 
    #         return bk_id
        
    #     # TODO : fix this implementation
    #     if bk_id == 0 or bk_id == "0":
    #         return bk_id
            
    #     return None        

    def pending_state(self,bk_id):

        if self.specluate_ledger.cache[bk_id] is not None:
            return bk_id 
        return None


    #commit the pending prefix of the given block id and prune other branches
    def commit(self,bk_id):
        print("[Ledger][replicaID {}] START commit ".format(self.replicaID)) 
        block_id = bytes(str(bk_id),'utf-8')
        entry = self._db_speculate.get(block_id)        
        if  entry is not None:
            print("[Ledger][replicaID {}] Commited block {}.".format(self.replicaID, bk_id)) 
            self._db.put(block_id,entry)
            # self._db_speculate.delete(block_id)      
        print("[Ledger][replicaID {}] END commit ".format(self.replicaID)) 


    #returns a committed block given its id
    def committed_block(self, block_id):
        print("[Ledger][replicaID {}] START committed_block ".format(self.replicaID)) 
        block_id=bytes(str(block_id),'utf-8')
        print("[Ledger][replicaID {}] END committed_block ".format(self.replicaID))
        entry = pickle.loads(self._db.get(block_id))

        return entry[1]


    def print_ledger(self):
        
        it =  self._db.iterator()
        with self._db.iterator() as it:
            for k,v  in it:
                print(k,v)