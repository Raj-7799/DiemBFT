import plyvel

class Ledger():

    def __init__(self,genesis_block, replicaID):
        self.replicaID = replicaID
        self._db = plyvel.DB('/tmp/diemLedger_{}/'.format(self.replicaID), create_if_missing=True)
        self._db_speculate = plyvel.DB('/tmp/diemLedger_speculate_{}/'.format(self.replicaID), create_if_missing=True)
        self.speculate(genesis_block.id,genesis_block.id,genesis_block)
        self.commit(genesis_block.id)
        


    # apply txns speculatively
    def speculate(self,prev_block_id, block_id, txns):
        block_id=bytes(str(block_id),'utf-8')
        value = bytes(str([prev_block_id,txns]),'utf-8')        
        self._db_speculate.put(block_id,value)


    #find the pending state for the given block id or ⊥ if not present
    def pending_state(self,block_id):
        block_id = bytes(str(block_id),'utf-8')     
        entry = self._db_speculate.get(block_id)
        if entry is not None:
            return block_id
        return None                


    #commit the pending prefix of the given block id and prune other branches
    def commit(self,block_id):
        block_id = bytes(str(block_id),'utf-8')
        entry = self._db_speculate.get(block_id)        
        if  entry is not None:
            self._db.put(block_id,entry)
            self._db_speculate.delete(block_id)                   


    #returns a committed block given its id
    def committed_block(self,block_id):
        block_id=bytes(str(block_id),'utf-8')
        return self._db_speculate.get(block_id)        


    def print_ledger(self):
        
        it =  self._db.iterator()
        with self._db.iterator() as it:
            for k,v  in it:
                print(k,v)