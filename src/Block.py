class Block:

    def __init__(self,author,round,payload,qc,id):
        self._author=author
        self._round=round
        self._payload=payload
        self._qc = qc 
        self._id =id 