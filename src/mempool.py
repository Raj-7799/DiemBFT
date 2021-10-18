from collections import deque
import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class MemPool:
    def __init__(self,OutputMempool):
        self.queue = deque([])
        self.locator = {}
        self.state = set()
        self.OutputMempool=OutputMempool
    
    def get_transactions(self):
        # currently only sends one transaction
        self.OutputMempool("[get_transactions] Entry ")
        if self.queue:
            command = self.queue.popleft()
            if command in self.locator and command not in self.state:
                self.state.add(command)
                self.OutputMempool("[get_transactions] Exit with command {} from queue  ".format(command))
                return command
            else:
                return self.get_transactions()
        else:
            self.OutputMempool("[get_transactions] Exit queue empty ")

            return None

    def markState(self, command):
        self.state.add(command)
    
    def insert_command(self, command, client):
        self.OutputMempool("[insert_command] command {}".format(command))

        if command not in self.locator and command not in self.state:
            self.queue.append(command)
            self.locator[command] = client
        else:
            self.OutputMempool("[insert_command] Command already present in mempool")

    def delete_command(self, command):
        self.OutputMempool("[delete_command] Delete {} from Mempool".format(command))
        if command in self.locator:
            self.OutputMempool("[delete_command] Delete {} from Mempool Successfull".format(command))
            del self.locator[command]

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