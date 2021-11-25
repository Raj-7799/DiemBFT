import random
from collections import defaultdict

R = 10 # total number of rounds
M = 3 # max partitions per round
F = 1 # number of twins
probability_of_overlap = 0.5 # probability of overlapping partition
probability_partition_has_overlap = 0.5 # probability that a network partition contains a overlap


total_nodes = 3 * F + 1
Partitions = []

def assign_leaders(type = "random", assignments = {}):

    '''
    assign leaders assigns leaders at each round. 
    type = random does random assignments for each rounds
    type = sequential does sequential assigments starting from leader 1

    assignments is a dictionary which can be used to deterministically to assign leaders at each round
    '''

    # if not (len(assignments) <= R and max(assignments) <= R):
    #     print("Leader assignments should not exceed round numbers")
    #     return None

    pending_assignments = []
    final_assignments = {}

    for i in range(1, R + 4):
        if i not in assignments:
            pending_assignments.append(i)
        
    if type == "sequential":
        for  i in range(1, R + 1):
            if i not in assignments:
                final_assignments[i] = i % total_nodes
            else:
                final_assignments[i] = assignments[i]
    elif type == "random":
        for  i in range(1, R + 1):
            if i not in assignments:
                final_assignments[i] = random.randint(0, total_nodes-1)
            else:
                final_assignments[i] = assignments[i]
    else:
        print("invalid type for leader assignments")
        return None
    
    return final_assignments

def liveness_properties(assignments = [], blocks_to_commit = 1):
    '''
    Live properties determines the total blocks to commit and at which rounds they have to be committed
    assignments is an array which can be used to speciy which rounds to commit a block
    blocks_to_commit dictates how many blocks should be committed
    '''

    if len(assignments) >= blocks_to_commit or len(assignments) > R - 2 or max(assignments) > R - 2 or min(assignments) < 3:
        print("invalid assignment for round block commits")
        return None
    
    assignments_remaining = blocks_to_commit - len(assignments)
    rounds_remaining = []
    final_assignments = [].extend(assignments)

    for i in range(3, R - 2):
        if i not in assignments:
            rounds_remaining.append(i)
    
    final_assignments.extend(random.sample(rounds_remaining, assignments_remaining))

    return final_assignments

import copy
def generatePartitionRec(index, arr, current_partition, partitions):
    if index == len(arr):
        partitions.append(copy.deepcopy(current_partition))
    else:
        current_partition[-1].append(arr[index])
        generatePartitionRec(index+1, arr, current_partition, partitions)

        current_partition[-1].pop()
        new_partition = []
        new_partition.append(arr[index])
        current_partition.append(new_partition)
        generatePartitionRec(index+1, arr, current_partition, partitions)
        current_partition.pop()

def generatePartition(Set):
    current_partition = []
    current_partition.append([Set[0]])
    generatePartitionRec(1, Set, current_partition, Partitions)

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
    arr = [i for i in range(N + F)]
    current_partition = []
    current_partition.append([arr[0]])
    partitions = []
    generatePartitionRec(1, arr, current_partition, partitions)

    partitions = prune_duplicate_partition(partitions)
    majority_partitions = get_majority_partitions(partitions, F)

    return partitions, majority_partitions

def populate_partition(network_partition):
    nodes = [i for i in range(total_nodes + F)]
    node_shuffled = random.sample(nodes, total_nodes + F)

    no_of_partitions = len(network_partition)
    i = 0
    k = 0

    while i < no_of_partitions:
        partition_size = len(network_partition[i])
        j = 0
        while j < partition_size:
            network_partition[i][j] = node_shuffled[k]
            j += 1
        
        k += 1
        
    # add overlaps based on probability
    if random.uniform(0, 1) < probability_of_overlap:
        for i in range(network_partition):
            if random.uniform(0, 1) < probability_partition_has_overlap:
                non_partition_nodes = set(node_shuffled) - set(network_partition[i])
                network_partition[i].append(list(random.choice(non_partition_nodes)))
    
    return network_partition   

def populate_conensus_partition(network_partition, leader, twin_nodes):
    '''
    this can contain twins in majority partition
    '''
    nodes = [i for i in range(total_nodes + F)]
    nodes_shuffled = set(random.sample(nodes, total_nodes + F))

    if len(network_partition) == 1:
        return nodes
    
    majority_partition = network_partition[0]
    # place the leader in majority partition
    majority_partition[0] = leader
    nodes_shuffled.remove(leader)
    # remove twin nodes from node shuffled
    nodes_shuffled -= twin_nodes

    i = 1
    # forming the majority partition
    while i < len(majority_partition) and nodes_shuffled:
        select_node = nodes_shuffled.pop()
        majority_partition[i] = select_node
        
        if not nodes_shuffled:
            # if shuffle nodes become empty now place the twin nodes
            nodes_shuffled += twin_nodes
        
        i += 1

    for i in range(1, len(network_partition)):
        # fill up remaining partitions
        for j in range(len(network_partition[i])):
            network_partition[i][j] = nodes_shuffled.pop()
    
    return network_partition


def round_assignment(leader_assignments, twin_nodes, parition_assignments={}):
    # generate the number of partition per round
    partition_choices = [i for i in range(1, M + 1)]
    partition_per_round = {}

    for i in range(1, R + 1):
        partition_per_round[i] = random.choice(partition_choices)
    
    # generate all network partition scenarios from sum of total nodes and its twins
    partition_scenarios, major_partitions = get_partition_scenarios(total_nodes, F)
    # print("----------------")
    # print(partition_scenarios)
    # print("----------------")
    # print(major_partitions)
    # print("----------------")
    # print(leader_assignments)
    # print("----------------")

    final_assignments = {}

    for i in range(1, R + 4):
        final_assignments[i] = []
    for i in range(1, R + 1):
        # partitions can be populated randomly expect for last partition 
        if i in parition_assignments:
            final_assignments[i] = parition_assignments[i]
            continue
        
        for j in range(partition_per_round[i] - 1):
            # final_assignments[i].append(populate_partition(
            #     random.choice(partition_scenarios),
            #     leader_assignments[i]
            #     ))
            final_assignments[i].append(random.choice(partition_scenarios))
        
        # ensuring that the last partition trigger will have super majority
        final_assignments[i].append(populate_conensus_partition(
                random.choice(major_partitions),
                leader_assignments[i],
                twin_nodes
            ))
    
    # adding three extra rounds with super majority to ensure liveness
    for i in range(1, 4):
        final_assignments[R + i].append(populate_conensus_partition(
                random.choice(major_partitions),
                leader_assignments[i], 
                twin_nodes
        ))
    
    return final_assignments


# Set = ["1", "2", "3", "4"]
# generatePartition(Set)
# print(Partitions)
# Partitions = prune_duplicate_partition(Partitions)
# print(Partitions)
leader_assignments = assign_leaders()
print(leader_assignments)
for key,value in leader_assignments.items():
    print(value,",")
twin_nodes = set(["1"])
final_assignments = round_assignment(leader_assignments, twin_nodes)
for key, value in final_assignments.items():
    # print(key, ":", value)
    print(value,",")


