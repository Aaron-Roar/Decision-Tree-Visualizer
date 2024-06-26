import information_gain
import random
import graphviz
import math

#Linked List Structure
################################################
################################################
global_multi_list = []

class MultiList:
    def __init__(self, value):
        self.tokens = []
        self.nexts = []
        self.value = value
        self.previous = None

    def get_value(self):
        return self.value

    def get_token(self, value):
        for index, i in enumerate(self.nexts):
            if(value == i):
                return self.tokens[index]

    def get_tokens(self):
        return self.tokens

    def add_list(self, token, multi_list):
        self.tokens.append(token)
        global_multi_list.append(MultiList(multi_list))
        self.nexts.append(global_multi_list[len(global_multi_list) - 1])
        global_multi_list[len(global_multi_list) - 1].previous = self

    def add_lists(self, tokens, multi_lists):
        for index, token in enumerate(tokens):
            self.add_list(token, multi_lists[index])

    def get_list(self, token):
        return self.nexts[self.tokens.index(token)]
################################################
################################################

#Matrix Operations
################################################
################################################
def get_random_row(matrix):
    new_matrix = tokenize_matrix(matrix)
    random_row = int(100*random.random())%len(new_matrix)
    return new_matrix[random_row]

def get_cols(matrix, col):
    for row in matrix:
        yield row[col]

def remove_col(some_list, col):
    del some_list[col]
    return some_list

def remove_cols(old_matrix, col):
    matrix = list(old_matrix)
    for row in matrix:
        remove_col(row, col)

    return matrix
################################################
################################################

#Seperating By Attributes
################################################
################################################
def split_by_attribute(matrix, col):
    if(information_gain.float_test(list(get_cols(de_tokenize_matrix(matrix), col))) == True):
        return list(split_continous(list(matrix), col))
    else:
        return list(split_discrete(list(matrix), col))

def split_continous(matrix,col):
    #if(len(matrix[0]) <= 1):
        #print("cant split matrix any further [error!]\n")

    split_value = information_gain.value_of_best_split(de_tokenize_matrix(matrix), col)

    
    attributes = [
        str(str(matrix[0][col][0:matrix[0][col].index(":") + 1]) + "<" + str(split_value)),
        str(str(matrix[0][col][0:matrix[0][col].index(":") + 1]) + ">=" + str(split_value))
    ]

    splits = [[], []]
    for row in matrix:
        if(float(de_tokenize(row[col])) < float(split_value)):
            splits[0].append(remove_col(list(row), col))
        else:
            splits[1].append(remove_col(list(row), col))

    for index, value in enumerate(splits):
        if(value == []):
            attributes.pop(index)
            splits.pop(index)

    for index, value in enumerate(attributes):
        yield [value, splits[index]]


def split_discrete(matrix, col):
    #if(len(matrix[0]) <= 1):
        #print("cant split matrix any further [error!]\n")

    attributes = []
    splits = []

    for row in matrix:
        if(attributes.count(row[col]) == 0):
            attributes.append(row[col])
            splits.append([])
    
    for row in matrix:
        splits[attributes.index(row[col])].append(remove_col(list(row), col))

    for index, value in enumerate(attributes):
        yield [value, splits[index]]
################################################
################################################

#Leaf Creation
################################################
################################################
def make_leaf(multi_list):
    highest_key = 0
    highest_key_length = 0
    splits = split_by_attribute(list(multi_list.get_value()), len(multi_list.get_value()[0]) - 1)
    for index, key in enumerate(list(get_cols(splits, 0))):
        list_length = len(list(get_cols(splits, 1)))
        if(list_length > highest_key_length):
            highest_key_length = list_length
            highest_key = index
    multi_list.value = de_tokenize(list(get_cols(splits, 0))[highest_key])
    multi_list.nexts = None

def all_targets_true(matrix, target_col):
    prev_value = matrix[0][target_col]
    for value in get_cols(matrix, target_col):
        if(value != prev_value):
            return False
    return True
################################################
################################################

#Tree Building
################################################
################################################
def branch_multi_list(multi_list, quality_func, determine_leaf_func):
    if(multi_list.nexts == None):
        make_leaf(multi_list)
        return -1
    if(multi_list.value == []):
        make_leaf(multi_list)
        return -1
    if(multi_list.value == None):
        make_leaf(multi_list)
        return -1
    if(multi_list.tokens == None or multi_list.tokens == []):
        make_leaf(multi_list)
        return -1

    if(len(multi_list.value[0]) <= 1):
        make_leaf(multi_list)
        return -1

    if(all_targets_true(de_tokenize_matrix(multi_list.get_value()), len(multi_list.get_value()[0]) - 1) == True):
        make_leaf(multi_list)
        return -1

    splits = list(split_by_attribute(list(multi_list.get_value()), quality_func(de_tokenize_matrix(multi_list.get_value()))))

    multi_list.add_lists(
        list(get_cols(splits, 0)), 
        list(get_cols(splits, 1))
    )

    return 1

def reccursive_branch(multi_list, qual_func, leaf_func): #algorithm is the algorithm to determin what attribute is highest IG
    if(branch_multi_list(multi_list, qual_func, leaf_func) != -1):
        leaf_func(multi_list)#) #In the case of ID3 makes all lefes that have next lower information gain a leaf
        for token in multi_list.get_tokens():
            reccursive_branch(multi_list.get_list(token), qual_func, leaf_func)
################################################
################################################

#Tree Graphing
################################################
################################################
dot = graphviz.Digraph()

def evaluate_graphviz_tree(multi_list, prev_node, edges):
    if(multi_list.nexts == None or multi_list.value == [] or multi_list.value == None or multi_list.tokens == None):
        dot.node(str(multi_list), str(multi_list.get_value()), shape = 'doublecircle')
        dot.edge(str(prev_node), str(multi_list), label = str(prev_node.get_token(multi_list)))
    
    elif(prev_node == None):
        dot.node(str(multi_list), str(multi_list.tokens), shape = 'ellipse')
    
        for next_multi_list in multi_list.nexts:
            evaluate_graphviz_tree(next_multi_list, multi_list, edges)

    else:

        dot.node(str(multi_list), str(multi_list.tokens), shape = 'circle')
        dot.edge(str(prev_node), str(multi_list), label = str(prev_node.get_token(multi_list)))
    
        for next_multi_list in multi_list.nexts:
            evaluate_graphviz_tree(next_multi_list, multi_list, edges)

def export_tree_graphviz(multi_list):
    edges = []
    evaluate_graphviz_tree(multi_list, None, edges)
    dot.render("tree.gv")
################################################
################################################

#Tree evaluation
################################################
################################################
def evaluate_tree_continous(input_token, list_tokens):
    for list_token in list_tokens:
        if(eval(str(input_token) + str(list_token))):
            return list_tokens.index(list_token)
    print("Ran out of tokens")
    return None

def evaluate_tree_discrete(input_token, list_tokens):
    if(list_tokens.count(input_token) != 0):
        return list_tokens.index(input_token)
    return None

def evaluate_tree(multi_list, input_tokens):
    if(multi_list.nexts == None): #previously had len(multi_lists.nexts)
        return multi_list.get_value()

    for input_index, input_token in enumerate(input_tokens):
        for list_token in multi_list.tokens:
            if(input_token.count(":") == 0 or list_token.count(":") == 0):
                return None
            if(input_token[:input_token.index(":")] == list_token[:list_token.index(":")]):

                input_tokens.pop(input_index)
                if(information_gain.float_test(de_tokenize(input_token))):

                    tree_cont = evaluate_tree_continous(de_tokenize(input_token), list(de_tokenize_list(multi_list.tokens)))
                    if(tree_cont == None):
                        return None
                    return evaluate_tree(multi_list.get_list(multi_list.tokens[tree_cont]), input_tokens)

                else:
                    tree_disc = evaluate_tree_discrete(de_tokenize(input_token), list(de_tokenize_list(multi_list.tokens)))
                    if(tree_disc == None):
                        return None
                    return evaluate_tree(multi_list.get_list(multi_list.tokens[tree_disc]), input_tokens)

    print("Failed to find token")
    return None

def evaluate_forest_target(trees, input_tokens):
    evaluations = []
    for tree in trees:
        evaluations.append(evaluate_target(tree, input_tokens))

    highest_value = [0, None]
    for value in evaluations:
        if(highest_value[0] < evaluations.count(value)):
            highest_value[0] = evaluations.count(value)
            highest_value[1] = value

    return highest_value[1]


def evaluate_target(multi_list, list_tokens):
    return evaluate_tree(multi_list, tokenize_row(list_tokens))

################################################
################################################

#Leaf_Determination Algorithm
################################################
################################################
def id3_greedy_search(multi_lists):
    return 0

def weak_learner(multi_lists):
    for multi_list in multi_lists.nexts:
        make_leaf(multi_list)
################################################
################################################

#Branching Algorithms
################################################
################################################
def random_compare(matrix):
    return random.randrange(0, len(matrix[0]) - 1, 1)

def ig_compare(matrix):
    max_ig_col = [0,0] #[value_of_ig, column]
    i = 0
    while(i < len(matrix[0]) - 1):
        ig = information_gain.Information_Gain(matrix, i)
        if(ig > max_ig_col[0]):
            max_ig_col[0] = ig
            max_ig_col[1] = i
        i = i + 1
    return max_ig_col[1]
################################################
################################################

#Creating Tokens for Attributes
################################################
################################################
def tokenize_matrix(old_matrix):
    matrix = []
    for row in old_matrix:
        matrix.append(list(row))
    for row in matrix:
        for index, col in enumerate(row):
            row[index] = str(str(index) + ":" + str(col))
    return matrix

def tokenize_row(tokens):
    new_tokens = []
    for index, token in enumerate(tokens):
        new_tokens.append(str(str(index) + ":" + str(token)))
    return new_tokens

def de_tokenize(value):
    return value[value.index(":") + 1:]

def de_tokenize_list(old_list):
    for i in list(old_list):
        yield de_tokenize(i)

def de_tokenize_matrix(old_matrix):
    matrix = []
    for row in old_matrix:
        matrix.append(list(row))

    for row in matrix:
        for index, col in enumerate(row):
            row[index] = de_tokenize(col) 
    return matrix
################################################
################################################

#Decision Tree Interface
################################################
################################################
def adaboosts(multi_list, branch_selector, leaf_creator, counter):
    if(counter <= 0):
        return multi_list
    return adaboosts(adaboost(multi_list, branch_selector, leaf_creator), branch_selector, leaf_creator, counter -1)

def adaboosts_forest(trees, branch_selector, leaf_creator, counter):
    boosted_trees = []
    for tree in trees:
        boosted_trees.append(adaboosts(tree, branch_selector, leaf_creator, counter))
    return boosted_trees
    
def adaboost(multi_list, branch_selector, leaf_creator):
    def change_weight(imp, weight):
        return weight*math.exp(imp)
    def change_weights(imp, index_list, weights):
        for index in index_list:
            weights[index] = change_weight(imp, weights[index])
    def normalize_weights(weights):
        weight_sum = sum(weights)
        for index, weight in enumerate(weights):
            weights[index] = weight/weight_sum
    def create_bucket(weights, bucket):
        for index, weight in enumerate(weights):
            if((index + 1) == len(weights)):
                bucket.append(1)
            else:
                bucket.append(sum(weights[:(index + 1)]))
    def build_new_matrix(multi_list, bucket):
        new_matrix = []
        i = 0
        while(i < len(multi_list.get_value())):
            rand_value = random.random()
            for index, value in enumerate(bucket):
                if(rand_value < value):
                    new_matrix.append(multi_list.get_value()[index])
                    break
            i = i + 1

        return new_matrix

    weight_list = []
    bucket_list = []
    split = [[],[]] #Correct, Incorrect

    i = 0
    while(i < len(multi_list.get_value())):
        weight_list.append(float(1/len(multi_list.get_value())))
        i = i + 1

    for index, row in enumerate(multi_list.get_value()):
        if(de_tokenize(row[len(row) - 1]) == evaluate_tree(multi_list, list(row))):
            split[0].append(index)
        else:
            split[1].append(index)

    if(len(split[1]) != 0 and len(split[0]) != len(split[1])):
        total_error = len(split[1])/len(multi_list.get_value())
        importance = (1/2)*math.log((1 - total_error)/total_error, 10)

        change_weights(-importance, split[0], weight_list)
        change_weights(importance, split[1], weight_list)
        normalize_weights(weight_list)
        create_bucket(weight_list, bucket_list)
        new_multi_list = MultiList(build_new_matrix(multi_list, bucket_list))
        reccursive_branch(new_multi_list, branch_selector, leaf_creator)

        return new_multi_list
    return multi_list

def random_forest(old_matrix, tree_amount, compare, search):
    matrix = tokenize_matrix(old_matrix)
    data_sets = []
    instances = int(len(matrix)/tree_amount)

    i = 0
    matrix_rows = len(matrix)
    while(i < tree_amount):
        data_sets.append([])
        j = 0
        while(j < instances):
            data_sets[i].append(matrix.pop(0))
            j = j + 1
        i = i + 1

    for value in data_sets[:len(data_sets)]:
        tree = MultiList(value)
        reccursive_branch(tree, compare, search)
        yield tree

def build_tree(matrix, branch_selector, leaf_creator):
    tree = MultiList(tokenize_matrix(matrix))
    reccursive_branch(tree, branch_selector, leaf_creator)
    return tree
################################################
################################################

training_matrix = [
["Sunny",    "85", "85", "Weak",   "No"],
["Sunny",    "80", "90", "Strong", "No"],
["Overcast", "83", "78", "Weak",   "Yes"],
["Rain",     "70", "96", "Weak",   "Yes"],
["Rain",     "68", "80", "Weak",   "Yes"],
["Rain",     "65", "70", "Strong", "No"],
["Overcast", "64", "65", "Strong", "Yes"],
["Sunny",    "72", "95", "Weak",   "No"],
["Sunny",    "69", "70", "Weak",   "Yes"],
["Rain",     "75", "80", "Weak",   "Yes"],
["Sunny",    "75", "70", "Strong", "Yes"],
["Overcast", "72", "90", "Strong", "Yes"],
["Overcast", "81", "75", "Weak",   "Yes"],
["Rain",     "71", "80", "Strong", "No"]
]

test_matrix = [
["Overcast", "83", "78", "Weak",   "Yes"],
["Sunny",    "69", "70", "Weak",   "Yes"],
["Rain",     "70", "96", "Weak",   "Yes"],
["Overcast", "72", "90", "Strong", "Yes"],
["Rain",     "71", "80", "Strong", "No"],
["Rain",     "68", "80", "Weak",   "Yes"]
]

def tree_target_evaluations(tree, testing_matrix):
    for row in testing_matrix:
        yield [row[len(row) - 1], evaluate_target(tree, row)]

def tree_accuracy(tree, testing_matrix):
    target_evaluations = list(tree_target_evaluations(tree, testing_matrix))
    correct_instances = 0
    for row in target_evaluations:
        if(row[0] == row[1]):
            correct_instances = correct_instances + 1
    return correct_instances/len(target_evaluations)

def tree_accuracies(trees, testing_matrix):
    net_accuracy = 0
    for tree in trees:
        net_accuracy += tree_accuracy(tree, testing_matrix)
    return net_accuracy/len(trees)




######Example Create A Normal Decision tree and calculate accuracy
#tree = build_tree(test_matrix, ig_compare, id3_greedy_search)
#leaf = evaluate_target(tree, training_matrix[10]) #Save all tokens as the [column of attribute, token value]. This way you can have unique tokens with same values
#export_tree_graphviz(tree)
#print(leaf)
#print(tree_accuracy(tree, training_matrix))
######

######Example Random Forest of weak learners with random stump selection
#forest = list(random_forest(training_matrix, 3, ig_compare, weak_learner)) #make adaboost function which adaboosts a single tree, just changes the matrix relative to that tree
#leaf_forest = evaluate_forest_target(forest, test_matrix[1])
#print(tree_accuracies(forest, test_matrix))
#print(leaf_forest)
######

######Example Adaboost a tree
#tree = build_tree(training_matrix, random_compare, weak_learner)
#ada_boosted_tree = adaboosts(tree, random_compare, weak_learner, 2)
#leaf = evaluate_target(ada_boosted_tree, test_matrix[4]) #Save all tokens as the [column of attribute, token value]. This way you can have unique tokens with same values
#print(leaf)
######

######Example Adaboost a forest
#forest = list(random_forest(training_matrix, 3, random_compare, weak_learner)) #make adaboost function which adaboosts a single tree, just changes the matrix relative to that tree
#print(tree_accuracies(forest, test_matrix))
#boosted_forest = adaboosts_forest(forest, random_compare, weak_learner, 1)
#print(tree_accuracies(boosted_forest, test_matrix))
######

#####Example Graphing a Tree
#tree = build_tree(training_matrix, ig_compare, id3_greedy_search)
#export_tree_graphviz(tree)
#####



#Use this with file opening code from lab1
#Add a way to prune the data
