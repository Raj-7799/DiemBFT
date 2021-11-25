import json

class NetworkPlayground():



    def __init__(self):
        pass
    def setup(config:dict):
        pass



    def read_config(self,file):
        """
            Reading Config file 
        """
        config =  open(file)
        twin_config =  json.load(config)
        config.close()
        num_of_nodes = twin_config["num_of_nodes"]
        num_of_twins =  twin_config["num_of_twins"]
        scenarios =  twin_config["scenarios"]
        print(len(scenarios))
        return num_of_nodes,num_of_twins,scenarios

    
    def run():
        output("Creating {} Network PlayGround ")


file = "testcase-1-0-0.json"
network_playgroud =  NetworkPlayground()
network_playgroud.read_config(file)

