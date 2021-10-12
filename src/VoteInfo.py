class VoteInfo:

    def __init__(self, id: str, round: int, parent_id: str, parent_round: int, exec_state_id: str):
        self.id = id
        self.round = round
        self.parent_id = parent_id
        self.parent_round = parent_round
        self.exec_state_id = exec_state_id