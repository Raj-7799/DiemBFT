import threading


class RequestTimeoutHandler:
    def __init__(self, callback, process,OutputRequestTimeOutHandler):
        self.callback = callback
        self.process = process
        self.dict_of_timer = {} # dict of timer for a command
        self.OutputRequestTimeOutHandler=OutputRequestTimeOutHandler

    def _on_timeout(self, command):
        if command in self.dict_of_timer:
            del self.dict_of_timer[command]
        self.OutputRequestTimeOutHandler("Resending request {} to back on timeout".format(command))
        self.callback(command)

    def stop_timer(self, command):
        if command in self.dict_of_timer:
            self.OutputRequestTimeOutHandler("Stopping timer of client {} for command {}".format(self.process, command))
            self.dict_of_timer[command].cancel()
            del self.dict_of_timer[command]
        
        self.OutputRequestTimeOutHandler("Stopped timer of client {} for command {}".format(self.process, command))

    def start_timer(self, command, delta):
        if command in self.dict_of_timer:
            return
        
        self.OutputRequestTimeOutHandler("Starting timer of client {} for command {}".format(self.process, command))
        self.dict_of_timer[command] = threading.Timer(delta, self._on_timeout, [command])
        self.dict_of_timer[command].start()
        self.OutputRequestTimeOutHandler("Started timer of client {} for command {}".format(self.process, command))
