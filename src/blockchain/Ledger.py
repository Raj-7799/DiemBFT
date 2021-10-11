import plyvel

class Ledger():

    def __init__(self):
        self._db = plyvel.DB('/tmp/diemLedger/', create_if_missing=True)
        self._db_speculate = plyvel.DB('/tmp/diemLedger_speculate/', create_if_missing=True)



    


    # apply txns speculatively
    def speculate(self,prev_block_id, block_id, txns):
        pass


    #find the pending state for the given block id or ⊥ if not present
    def pending_state(self,block_id):
        pass


    #commit the pending prefix of the given block id and prune other branches
    def commit(self,block_id):
        block = self._db_speculate.get(block_id)
        if  block is not None:
            self._db.put(block_id,block)
            self._db_speculate.delete(block_id)                   


    #returns a committed block given its id
    def committed_block(self,block_id):
        pass