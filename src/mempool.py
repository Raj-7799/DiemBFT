from collections import deque
import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class MemPool:
    def __init__(self, OutputMempool):
        self.queue = deque([])
        self.commited_blocks = set()
        self.OutputMempool = OutputMempool
    
    def get_transactions(self):
        # currently only sends one transaction
        if self.queue:
            command = self.queue.popleft()
            self.OutputMempool("[get_transactions] Exit with command {} from queue  ".format(command))
            return command
        else:
            self.OutputMempool("[get_transactions] Exit queue empty ")
            return None

    def markState(self, command):
        if command in self.queue:
            self.OutputMempool("[get_transactions] Removing command {} from queue ".format(command))
            self.queue.remove(command)
    
    def insert_command(self, command):
        if command not in self.commited_blocks and command not in self.queue:
            self.queue.append(command)
            self.OutputMempool("[insert_command] command {}".format(command))
        else:
            self.OutputMempool("[insert_command] Command already present in mempool")

    def delete_command(self, command):
        self.commited_blocks.add(command)
        self.markState(command)

    def remove_transaction(self, command):
        self.delete_command(command)
    
    def __str__(self):
        output = []
        output.append("MemPool : Queue [ ")

        for q in self.queue:
            output.append("{}, ".format(str(q)))
        
        output.append(" ]")

        output.append(" Commited Blocks [ ")

        for q in list(self.commited_blocks):
            output.append("{}, ".format(str(q)))
        
        output.append(" ]")
        return "".join(output)