class Block:

    def __init__(self,author,round,payload,qc,id):
        self._author=author
        self._round=round
        self._payload=payload
        self._qc = qc 
        self._id =id 


    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self,author):
        self._author=author
    
    @property
    def round(self):
        return self._round
    
    @round.setter
    def round(self,round):
        self._round=round
    
    @property
    def payload(self):
        return self._payload
    
    @payload.setter
    def payload(self,payload):
        self._payload=payload

    @property
    def qc(self):
        return self._qc
    
    @payload.setter
    def qc(self,qc):
        self._qc=qc

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self,id):
        self._id=id


# b=Block(1,2,3,4,5)
# print(b.author)