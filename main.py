import decision_tree
import data_parser
import sys


matrix_set: list = data_parser.sort_data_file(sys.argv[1], sys.argv[2], int(sys.argv[3])/100) #(file, delimiter, %for training and testing)
matrix_set1: list = matrix_set[0]
matrix_set2: list = matrix_set[1]

print("********Single Tree output********")
tree = decision_tree.build_tree(matrix_set1, decision_tree.ig_compare, decision_tree.id3_greedy_search)
rand_row1 = decision_tree.get_random_row(matrix_set2)

leaf = decision_tree.evaluate_target(tree, rand_row1) #Save all tokens as the [column of attribute, token value]. This way you can have unique tokens with same values
print("Actual Value: " + str(rand_row1[len(rand_row1) - 1]))
print("Predicted Value: " + str(leaf))
print("Tree Accuracy: " + str(decision_tree.tree_accuracy(tree, matrix_set2)))
print("\n")


print("********Weak learning forest output********")
forest = list(decision_tree.random_forest(matrix_set1, 3, decision_tree.ig_compare, decision_tree.weak_learner)) #Created a forest of weak learners that use random stump selection
rand_row2 = decision_tree.get_random_row(matrix_set2)

leaf_forest = decision_tree.evaluate_forest_target(forest, matrix_set2[1]) #Creating
print("Actual Value: " + str(rand_row2[len(rand_row2) - 1]))
print("Predicted Value: " + str(leaf_forest))
print("Forest Accuracy: " + str(decision_tree.tree_accuracies(forest, matrix_set2)))
