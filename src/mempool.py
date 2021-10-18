from collections import deque
import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class MemPool:
    def __init__(self):
        self.queue = deque([])
        self.locator = {}
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
    
    def insert_command(self, command, client):
        if command not in self.commited_blocks and command not in self.queue:
            self.queue.append(command)
            self.locator[command] = client
            print("Inserted commmand into mempool", command)
        else:
            print("Command already present in mempool", command)
            print("Command in ", self.print(), self.commited_blocks)

    def delete_command(self, command):
        self.commited_blocks.add(command)

    def remove_transaction(self, command):
        self.delete_command(command)

    def validate_command(self, command):
        return command in self.locator
    
    def __str__(self):
        return "{} {}".format(self.queue, self.locator)
    
    def print(self):
        output = ""
        for q in self.queue:
            output += str(q)
        
        return output