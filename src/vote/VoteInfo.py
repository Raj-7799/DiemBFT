class VoteInfo:

    def __init__(self):
        self._id = None
        self._round = None
        self._parent_id = None
        self._parent_round = None
        self._exec_state_id = None


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @id.deleter
    def id(self):
        del self._id

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, round):
        self._round = round

    @round.deleter
    def round(self):
        del self._round

    @property
    def parent_id(self):
        return self._parent_id
    
 
    @parent_id.setter
    def parent_id(self,value):
        self._parent_id=value

    @parent_id.deleter
    def parent_id(self):
        del self._parent_id
    

    @property
    def parent_round(self):
        return self._parent_round
    

    @parent_round.setter
    def parent_round(self,value):
        self._parent_round=value

    @parent_round.deleter
    def parent_round(self):
        del self._parent_round
    

    @property
    def exec_state_id(self):
        return self._exec_state_id
    

    @exec_state_id.setter
    def exec_state_id(self,value):
        self._exec_state_id=value

    @exec_state_id.deleter
    def exec_state_id(self):
        del self._exec_state_id
    
