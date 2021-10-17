import threading


class TimerHandler:
    def __init__(self, broadcasting_to_replicas, clientID, timeout_value):
        self.broadcasting_to_replicas = broadcasting_to_replicas
        self.clientID = clientID
        self.timeout_value = timeout_value
        self.dict_of_timer = {} # dict of timer for a command
    
    def _get_client_timer(self):
        print("Getting client timer")
        return 0#self.timeout_value

    def _on_client_timeout(self, command):
        #command ="2"
        #pass
        #print("Getting client timeout for command = " + str(command.payload))
        if command in self.dict_of_timer:
            del self.dict_of_timer[command]
        self.broadcasting_to_replicas(command)

    def stop_timer_for_command(self, command):
        if command in self.dict_of_timer:
            print("Stopping timer of client {} for command {}".format(self.clientID, command))
            self.dict_of_timer[command].cancel()
            #del self.dict_of_timer[command]
        print("Stopped timer of client {} for command {}".format(self.clientID, command))

    def start_timer_for_command(self, command):
        if command in self.dict_of_timer:
            self.dict_of_timer[command].cancel()
            #del self.dict_of_timer[command]
        print("Starting timer of client {} for command {}".format(self.clientID, command))
        self.dict_of_timer[command] = threading.Timer(self._get_client_timer(), self._on_client_timeout, [command])
        print("Started timer of client {} for command {}".format(self.clientID, command))
        self.dict_of_timer[command].start()
        print("Started timer of client {} for command {}".format(self.clientID, command))

