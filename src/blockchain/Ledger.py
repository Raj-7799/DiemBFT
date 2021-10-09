class Ledger():

    def __init__(self):
        pass


    # apply txns speculatively
    def speculate(self,prev_block_id, block_id, txns): 
        pass


    #find the pending state for the given block id or ⊥ if not present
    def pending_state(self,block_id):
        pass


    #commit the pending prefix of the given block id and prune other branches
    def commit(self,block_id):
        pass


    #returns a committed block given its id
    def committed_block(self,block_id):
        pass