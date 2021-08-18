# read dataset
dataset_file = open('./dataset.txt', 'r')
dataset = [line.strip().split(' ') for line in dataset_file.readlines()]
dataset_file.close()

# lowering dataset size
dataset = dataset[:1000]

# get all the items in the dataset as lists (with length 1)
def get_all_items(dataset):
    dataset_length = len(dataset)
    line_number = 0
    items_set = []
    for trans in dataset:
        line_number += 1
        print(f'line {line_number} of {dataset_length} in dataset. founded items: {len(items_set)}')
        for item in trans:
            if [item] not in items_set:
                item = [item]
                items_set.append(item)

    return items_set

# check if all of the members of first list are in second list
# Ex1: first_list = [1,2] & second_list=[1,2,3,4,5] -> return True
# Ex2: first_list = [1,2] & second_list=[2,3,4,5] -> return False
def is_it_in(first_list, second_list):
    for i in first_list:
        if i not in second_list:
            return False
    
    return True


# check if the first_list is in the list of lists with the name of second_list
# Ex1: first_list = [1,2] & second_list = [ [[5,3],2] , [[1,2], 3] ] -> return True
# Ex2: first_list = [1,2] & second_list = [ [[5,3],2] , [[8,6], 1] ] -> return False
def is_in_list(first_list, second_list):
    for t in range(len(second_list)):
        if first_list == second_list[t][0]:
            return t
    
    return -1


# generate length (k+1) candidate itemset from length
# from length (k) frequent itemset
def new_candidate_itemset(old_dataset, pair_num):
    pair_num = pair_num - 1

    # change all items to a set
    itemset = []
    for i in old_dataset:
        for item in i:
            if item not in itemset:
                itemset.append(item)

    new_candidate_itemset = []

    # make itemsets with given pairnumber
    for i in range(len(itemset)-pair_num):
        m = i+1
        for j in range(len(itemset)-i-pair_num):
            temp = [itemset[i]]
            for item in itemset[m:m+pair_num]:
                temp.append(item)
            
            new_candidate_itemset.append(temp)
            
            m += 1

    return new_candidate_itemset


def find_frequent_itemsets(dataset, all_itemsets, min_support, K_item_set_length=1):
    """
    find frequent itemsets
    dataset -> list of records, each member in the dataset list is a list
    Ex: [[1,2,3],[2,3,4],[1,5,7], ...]

    all_itemsets -> list of all items in list
    Ex: [['35'], ['60'], ['50'], ...]

    min_support -> an integer number of minimum support for 

    K_item_set_length -> start number of itemsets length 
    Default = 1
    """

    frequent_itemsets = ['not empty']
    all_frequent_itemsets = []

    # for each itemsets that we have in this iteration we
    # search for it's frequence
    while len(frequent_itemsets) > 0:
        print("Itemsets length (K): ", K_item_set_length)

        itemsets_frequence = []
        itemset_number = 0
        for itemset in all_itemsets:
            itemset_number += 1
            print(f'checking itemset #{itemset_number} with K: {K_item_set_length}')
            
            for transaction in dataset:    
                if is_it_in(itemset, transaction):
        
                    is_in_res = is_in_list(itemset, itemsets_frequence)
                    if is_in_res >= 0:
                        itemsets_frequence[is_in_res][1] += 1
                    else:
                        itemsets_frequence.append([itemset, 1])

        # eliminate candidates that are infrequent
        frequent_itemsets = [t for t in itemsets_frequence if t[1]> min_support]

        # get only itemsets and not frequent count of them
        old_itemsets = [t[0] for t in frequent_itemsets]

        # give founded frequent itemsets to generate new itemsets with
        # new length (one more of their length size)
        K_item_set_length += 1
        all_itemsets = new_candidate_itemset(old_itemsets,K_item_set_length)
        
        # add new frequent itemsets to all_frequent_itemsets
        all_frequent_itemsets += [itemset for itemset in frequent_itemsets]
        
    return all_frequent_itemsets


# this function work just like new_candidate_itemset function 
# bnut just for one itemset
def poss_patt(old_dataset, pair_num):

    pair_num = pair_num - 1

    if pair_num == 0:
        new_dataset = [[item] for item in old_dataset ]
        return new_dataset
        

    # get itemset
    all_itemset = []
    for item in old_dataset:
        # for item in i:
        if item not in all_itemset:
            all_itemset.append(item)

    # print(all_itemset,end='\n\n')
    new_dataset = []

    # make dataset with needed pairnumber
    for i in range(len(all_itemset)-pair_num):
        k = i+1
        for j in range(len(all_itemset)-i-pair_num):
            temp = [all_itemset[i]]
            for item in all_itemset[k:k+pair_num]:
                temp.append(item)
            
            new_dataset.append(temp)
            
            k += 1

    # print(new_dataset)
    return new_dataset


# Find Rules and calculate confidence and support
def make_rules(frequent_itemsets):

    # for each frequent itemsets we calculate support and confidence
    for fq in frequent_itemsets:
        freq_itemset = fq[0]

        support = fq[1] / len(dataset)

        # don't check frequent itemsets with length of one
        if len(freq_itemset) == 1:
            continue

        for i in range(len(freq_itemset)):
            # get all
            pos_patt = poss_patt(freq_itemset, i+1)

            for patt in pos_patt:
                temp_freq_itemset = freq_itemset.copy()

                # remove pattern from temp freq itemset
                for item in patt:
                    temp_freq_itemset.remove(item)

                # Now we get the association rules
                if len(temp_freq_itemset) > 0:

                    contain_freq_itemset = 0
                    contain_freq_itemset_and_patt = 0
                    
                    for trans in dataset:
                        if is_it_in(temp_freq_itemset, trans):
                            contain_freq_itemset += 1
                            if is_it_in(patt, trans):
                                contain_freq_itemset_and_patt += 1

                    confidence = contain_freq_itemset_and_patt / contain_freq_itemset
                    
                    this_rule = [patt,temp_freq_itemset, support, confidence]
                    
                    # alert rules with confidence more than 0.8
                    if confidence > 0.8:
                        print('Rule: ', this_rule[0], '->', this_rule[1], '  S: ', this_rule[2], '  C: ', this_rule[3], '\t', '<----')
                    else:
                        print('Rule: ', this_rule[0], '->', this_rule[1], '  S: ', this_rule[2], '  C: ', this_rule[3])

        print('*'*50)



print("Getting All items. Please wait...")
all_items = get_all_items(dataset)

print("Finding frequent itemsets")
min_support = 20
start_K_itemsets_length = 1
frequent_itemsets = find_frequent_itemsets(dataset, all_items,min_support, start_K_itemsets_length)

print("Finding Rules")
make_rules(frequent_itemsets)

# This code has been written by Yasin Boloorchi