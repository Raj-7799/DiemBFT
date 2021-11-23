import copy
def generatePartitionRec(index, arr, current_partition, partitions):
    if index==len(arr):
        partitions.append(copy.deepcopy(current_partition))
    else:
        current_partition[-1].append(arr[index])
        generatePartitionRec(index+1, arr, current_partition, partitions)

        current_partition[-1].pop()
        new_partition=[]
        new_partition.append(arr[index])
        current_partition.append(new_partition)
        generatePartitionRec(index+1, arr, current_partition, partitions)
        current_partition.pop()

def prune_duplicate_partition(partitions):
    for p in partitions:
        p.sort(key=lambda x : -len(x))
    
    unqiue_partitions = {}

    for p in partitions:
        key = []
        for np in p:
            key.append(str(len(np)))

        key = "".join(key)
        if key not in unqiue_partitions:
            unqiue_partitions[key] = p

    partitions = list(unqiue_partitions.values())
    return partitions

def get_majority_partitions(partitions, F):
    majority_partitions = []
    for p in partitions:
        if len(p[0]) >= (2*F + 1):
            majority_partitions.append(p)
    
    return majority_partitions

def get_partition_scenarios(N, F):