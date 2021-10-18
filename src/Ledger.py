import plyvel
import pickle

import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class Ledger:

    def __init__(self,genesis_block, replicaID, memPool, specluate_ledger, clientResponseHandler,OutputLogger):
        print("LEDGER for replica {}".format(replicaID))
        self.replicaID = replicaID
        self.memPool = memPool
        self._db = plyvel.DB('/tmp/diemLedger_{}/'.format(self.replicaID), create_if_missing=True)
        self._db_speculate = plyvel.DB('/tmp/diemLedger_speculate_{}/'.format(self.replicaID), create_if_missing=True)
        self.specluate_ledger = specluate_ledger
        self.clientResponseHandler = clientResponseHandler
        self.speculate(genesis_block.id,genesis_block.id,genesis_block)
        self.commit(genesis_block.id)
        self.last_committed_block = genesis_block.id
        self.diem_logger = get_logger(os.path.basename(__file__),self.replicaID)
        self.diem_logger.info("Hello ")
        self.OutputLogger=OutputLogger
        self.OutputLogger("{} Hello ".format("Ledger "))

    # apply txns speculatively
    def speculate(self,prev_block_id, block_id, txns):
        print("[Ledger][replicaID {}] Speculating for prev block {} and current block {} ".format(self.replicaID, prev_block_id, block_id))
        block_id=bytes(str(block_id),'utf-8')
        value = pickle.dumps([prev_block_id,txns])      
        self._db_speculate.put(block_id,value,sync=True)  

    def pending_state(self,bk_id):

        if bk_id in self.specluate_ledger.cache.keys() or bk_id == 0 or bk_id=="0":
            return bk_id 
        return None


    #commit the pending prefix of the given block id and prune other branches
    def commit(self,bk_id):
        print("[Ledger][replicaID {}] START commit the block {}".format(self.replicaID, bk_id)) 
        #self.print_ledger()
        self.specluate_ledger.print_cache()
        block_id = bytes(str(bk_id),'utf-8')
        #entry = self._db_speculate.get(block_id)
        
        entry =  self.specluate_ledger.cache[bk_id] if bk_id in self.specluate_ledger.cache.keys() else None
        

        print("TRYING TO COMMIT {} {} ".format(bk_id,entry))
        if  entry is not None:
            print("[Ledger][replicaID {}] Commited block {}.".format(self.replicaID, bk_id)) 
            #self._db.put(block_id,entry)
            # TODO : fix this
            # self._db_speculate.delete(block_id)
            self._db.put(block_id,pickle.dumps([entry.prev_node_id,entry.block]))
            block = self.committed_block(bk_id)
            
            self.memPool.remove_transaction(block.payload)
            # returning tuple to client ,given tuples are immutatble it ensure object is untrampered
            self.clientResponseHandler((bk_id, block.payload,self.replicaID))
            # self._db_speculate.delete(block_id)      
            self.last_committed_block = bk_id

        print("[Ledger][replicaID {}] END commit ".format(self.replicaID)) 

    #returns a committed block given its id
    def committed_block(self, bk_id):
        print("[Ledger][replicaID {}] Attempting to fetch commited block {}.".format(self.replicaID, bk_id)) 
        block_id=bytes(str(bk_id),'utf-8')
        print("committed_block {}".format(bk_id))
        # self.print_ledger()
        entry = pickle.loads(self._db.get(block_id))
        if entry[1]:
            print("[Ledger][replicaID {}] Fetching commited block successfull {}.".format(self.replicaID, bk_id)) 
        else:
            print("[Ledger][replicaID {}] Failed fetching block {}.".format(self.replicaID, bk_id)) 
        
        return entry[1]


    def print_ledger(self):
        print("PRINTING LEDGER {} ".format(self.replicaID))
        it =  self._db.iterator()
        with self._db.iterator() as it:
            for k,v  in it:
                print("key: {}  value {}".format(k,pickle.loads(v)[1]))

    

    def get_next_block(self,id):
        it = self._db.iterator(include_key=False)
        it.seek(bytes(str(id)),"utf-8")
        block = next(it)
        it.close()
        if block is not None:

            return pickle.loads(block)[1]
        