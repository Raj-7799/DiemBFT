import plyvel

replicaID=0
_db = plyvel.DB('/tmp/diemLedger_{}/'.format(replicaID), create_if_missing=True)

with _db.iterator() as it:
    for k,v in it:
        print(k,v)