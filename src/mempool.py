from collections import deque
import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class MemPool:
    def __init__(self):
        self.queue = deque([])
        self.locator = {}
        self.state = set()
    
    def get_transactions(self):
        # currently only sends one transaction
        if self.queue:
            command = self.queue.popleft()
            if command in self.locator and command not in self.state:
                self.state.add(command)
                return command
            else:
                return self.get_transactions()
        else:
            return None

    def markState(self, command):
        self.state.add(command)
    
    def insert_command(self, command, client):
        if command not in self.locator and command not in self.state:
            self.queue.append(command)
            self.locator[command] = client
        else:
            print("Command already present in mempool")

    def delete_command(self, command):
        print("Delete {} from Mempool".format(command))
        if command in self.locator:
            print("Delete {} from Mempool Successfull".format(command))
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