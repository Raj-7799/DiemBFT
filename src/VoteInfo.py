class VoteInfo:

    def __init__(self, id, round: int, parent_id, parent_round: int, exec_state_id):
        self.id = id
        self.round = round
        self.parent_id = parent_id
        self.parent_round = parent_round
        self.exec_state_id = exec_state_id