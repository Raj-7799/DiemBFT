import plyvel



import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class Ledger():

    def __init__(self,genesis_block, replicaID):
        self.replicaID = replicaID
        self._db = plyvel.DB('/tmp/diemLedger_{}/'.format(self.replicaID), create_if_missing=True)
        self._db_speculate = plyvel.DB('/tmp/diemLedger_speculate_{}/'.format(self.replicaID), create_if_missing=True)
        self.speculate(genesis_block.id,genesis_block.id,genesis_block)
        self.commit(genesis_block.id)
        


    # apply txns speculatively
    def speculate(self,prev_block_id, block_id, txns):
        diem_logger.info("[Ledger][replicaID {}] START speculate ".format(self.replicaID))
        block_id=bytes(str(block_id),'utf-8')
        value = bytes(str([prev_block_id,txns]),'utf-8')        
        self._db_speculate.put(block_id,value)
        diem_logger.info("[Ledger][replicaID {}] END speculate ".format(self.replicaID))



    #find the pending state for the given block id or ⊥ if not present
    def pending_state(self,block_id):
        diem_logger.info("[Ledger][replicaID {}] START pending_state ".format(self.replicaID)) 
        block_id = bytes(str(block_id),'utf-8')     
        entry = self._db_speculate.get(block_id)
        if entry is not None:
            diem_logger.info("[Ledger][replicaID {}] END pending_state ".format(self.replicaID)) 
            return block_id
        diem_logger.info("[Ledger][replicaID {}] END pending_state ".format(self.replicaID)) 
        return None                


    #commit the pending prefix of the given block id and prune other branches
    def commit(self,block_id):
        diem_logger.info("[Ledger][replicaID {}] START commit ".format(self.replicaID)) 
        block_id = bytes(str(block_id),'utf-8')
        entry = self._db_speculate.get(block_id)        
        if  entry is not None:
            self._db.put(block_id,entry)
            self._db_speculate.delete(block_id)
        diem_logger.info("[Ledger][replicaID {}] END commit ".format(self.replicaID)) 
             


    #returns a committed block given its id
    def committed_block(self,block_id):
        diem_logger.info("[Ledger][replicaID {}] START committed_block ".format(self.replicaID)) 
        block_id=bytes(str(block_id),'utf-8')
        diem_logger.info("[Ledger][replicaID {}] END committed_block ".format(self.replicaID)) 
        return self._db_speculate.get(block_id)        


    def print_ledger(self):
        
        it =  self._db.iterator()
        with self._db.iterator() as it:
            for k,v  in it:
                print(k,v)