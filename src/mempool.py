from collections import deque
import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class MemPool:
    def __init__(self):
        self.queue = deque([])
        self.locator = {}
    
    def get_transactions(self):
        # currently only sends one transaction
        if self.queue:
            command = self.queue.popleft()
            if command in self.locator:
                return command
            else:
                self.get_transactions()
        else:
            return None

    def insert_command(self, command, client):
        if command not in self.locator:
            self.queue.append(command)
            self.locator[command] = client

    def delete_command(self, command):
        print("Delete {} from Mempool".format(command))
        if command in self.locator:
            print("Delete {} from Mempool Successfull. Retrieved client {}".format(command, client))
            del self.locator[command]
            print("Deleted {} from Mempool. Retrieved client {}".format(command, client))
            return client
        
        return None

    def remove_transaction(self, command):
        self.delete_command(command)

    def validate_command(self, command):
        return command in self.locator
    
    def __str__(self):
        return "{} {}".format(self.queue, self.locator)