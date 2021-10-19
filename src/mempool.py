from collections import deque
import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class MemPool:
    def __init__(self):
        self.queue = deque([])
        self.commited_blocks = set()
    
    def get_transactions(self):
        # currently only sends one transaction
        if self.queue:
            command = self.queue.popleft()
            print("Returning command ", command, self.print(), self.commited_blocks)
            return command
        else:
            return None

    def markState(self, command):
        if command in self.queue:
            self.queue.remove(command)
    
    def insert_command(self, command):
        if command not in self.commited_blocks and command not in self.queue:
            self.queue.append(command)
            print("Inserted commmand into mempool", command)
        else:
            print("Command either commited or already present in mempool", command)

    def delete_command(self, command):
        self.commited_blocks.add(command)

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