class VoteInfo:

    def __init__(self, id: int, round: int, parent_id: int, parent_round: int, exec_state_id: int):
        self.id = id
        self.round = round
        self.parent_id = parent_id
        self.parent_round = parent_round
        self.exec_state_id = exec_state_id