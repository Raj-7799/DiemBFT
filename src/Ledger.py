import plyvel
import pickle

import os


class Ledger:

    def __init__(self,genesis_block, replicaID, memPool, specluate_ledger, clientResponseHandler,OutputLogger):
        self.replicaID = replicaID
        self.memPool = memPool
        self._db = plyvel.DB('/tmp/diemLedger_{}/'.format(self.replicaID), create_if_missing=True)
        self._db_speculate = plyvel.DB('/tmp/diemLedger_speculate_{}/'.format(self.replicaID), create_if_missing=True)
        self.specluate_ledger = specluate_ledger
        self.clientResponseHandler = clientResponseHandler
        self.speculate(genesis_block.id,genesis_block.id,genesis_block)
        self.commit(genesis_block.id)
        self.last_committed_block = genesis_block.id

        self.OutputLogger=OutputLogger
        

    # apply txns speculatively
    def speculate(self,prev_block_id, block_id, txns):
        block_id=bytes(str(block_id),'utf-8')
        value = pickle.dumps([prev_block_id,txns])      
        self._db_speculate.put(block_id,value,sync=True)  


    #// find the pending state for the given block id or ⊥ if not present
    def pending_state(self,bk_id):
        if bk_id in self.specluate_ledger.cache.keys() or bk_id == 0 or bk_id=="0":
            return bk_id 
        return None

    #commit the pending prefix of the given block id and prune other branches
    def commit(self,bk_id):
        block_id = bytes(str(bk_id),'utf-8')
        
        # fetch block from speculate ledger cache
        entry =  self.specluate_ledger.cache[bk_id] if bk_id in self.specluate_ledger.cache.keys() else None
        if  entry is not None:
            # commit the block
            self._db.put(block_id,pickle.dumps([entry.prev_node_id,entry.block]))
            block = self.committed_block(bk_id)
            print("[commit][ReplicaID [{}]] Commited block {} at round {}".format(self.replicaID, bk_id, block.roundNo))
            # setting transaction into mempool committed blocks cache
            self.memPool.remove_transaction(block.payload)
            # returning tuple to client ,given tuples are immutatble it ensure object is untrampered
            self.clientResponseHandler((bk_id, block.payload,self.replicaID))
            self.last_committed_block = bk_id


    #returns a committed block given its id
    def committed_block(self, bk_id):
        block_id=bytes(str(bk_id),'utf-8')
        ledger_entry = self._db.get(block_id)
        if ledger_entry:
            entry = pickle.loads(ledger_entry)
            return entry[1]
        else:
            return None

    def print_ledger(self):
        it =  self._db.iterator()
        with self._db.iterator() as it:
            for k,v  in it:
                print("key: {}  value {}".format(k,pickle.loads(v)[1]))

    def get_next_block(self,id):
        it = self._db.iterator(include_key=False)
        it.seek(bytes(str(id),'utf-8'))
        block = next(it)
        it.close()
        if block is not None:
            return pickle.loads(block)[1]
        