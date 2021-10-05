class VoteInfo:

    def __init__(self):
        self._id=None
        self._parent_id=None
        self._parent_round=None
        self._exec_state_id=None


    @property
    def id(self):
        return self._id
    

    @id.setter
    def id(self,value):
        self._id=value

    @id.deleter
    def id(self):
        del self._id
    
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
    
