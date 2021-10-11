class VoteInfo:

    def __init__(self,id,round_,parent_id,parent_round,exec_state_id):
        self._id = id
        self._round = round_
        self._parent_id = parent_id
        self._parent_round = parent_round
        self._exec_state_id = exec_state_id


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

    @id.setter
    def round(self, round):
        self._round = round

    @id.deleter
    def round(self):
        del self._round

    @property
    def parent_id(self):
        return self._parent_id
    
 
    @id.setter
    def parent_id(self,value):
        self._parent_id=value

    @id.deleter
    def parent_id(self):
        del self._parent_id
    

    @property
    def parent_round(self):
        return self._parent_round
    

    @id.setter
    def parent_round(self,value):
        self._parent_round=value

    @id.deleter
    def parent_round(self):
        del self._parent_round
    

    @property
    def exec_state_id(self):
        return self._exec_state_id
    

    @id.setter
    def exec_state_id(self,value):
        self._exec_state_id=value

    @id.deleter
    def exec_state_id(self):
        del self._exec_state_id
    
