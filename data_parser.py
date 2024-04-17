import sys
import random

#Prints the matrix to the screen
def print_matrix(matrix: list):
    for index, value in enumerate(matrix):
        print(str(matrix[index]) + "\n")

#Moves a value in a list from one spot to another
def translate(some_list: list, cur_loc, new_loc):
    value = some_list[cur_loc]
    del some_list[cur_loc]
    some_list.insert(new_loc, value)

#Moves values in a list from one spot to another spot
def translate_many(some_lists, cur_locs, new_locs):
    for some_list in some_lists: translate(some_list, cur_locs, new_locs) #Using translate on each row of the matrix

#Turns a file with data into a randomised matrix
def sort_data_file(file: str, delimiter: str, percent: float):
    with open(file, "r") as f: #Opening the file
        matrix: list = rand_split_data(
            list(parse_matrix(f.read(), delimiter)),
            percent
        ) #Parsing the matrix
        return (matrix[0], rand_split_data(matrix[1], 1)[0]) #Returning the first randomised set and the randomised second set

#Writes a matrix to a file in CSV format using the <,> symbol
def write_to_file(file: str, matrix: list):
    file = open(file, "w")

    for some_list in matrix:
        for index in range(len(some_list)):
            file.write(some_list[index])
            if(index != len(some_list) - 1):
                file.write(",") #Writing a <,> between each column
        file.write("\n") #Writing a <\n> for each row

    file.close()


#Turns a string in a CSV like format to a matrix with a user specified delimiter
def parse_matrix(string: str, col_symbol: str) -> map: #add row symbol support
    return map(
        lambda line: line.split(col_symbol),
        string.splitlines()
    ) #Creates a list of each new line in a string, and splits each line in the list into seperate values denoted by a symbol typically <,> or <\ >

#Calculated the dimensions of a 2D matrix
def matrix_dim(multi_list: list) -> tuple:
    return (len(multi_list), len(multi_list[0])) #[rows, cols]

#Randomly splits a matrix into two sets at a specified percent size difference
def rand_split_data(matrix: any, percent: float) -> list:
    init_set: list = list(matrix)
    new_set: list = []

    for i in range(int(matrix_dim(init_set)[0]*percent)):
        rand: int = int(random.random() * 1000) % matrix_dim(init_set)[0] #A random value within the index range of the rows of the matrix
        new_set.append(init_set[rand])
        del init_set[rand]

    return (new_set, init_set) #Retruning the randomised spliting of the matrix in two sets



#if(len(sys.argv) > 7):
#    translate_many(matrix_set1, int(sys.argv[6]), int(sys.argv[7]))
#    translate_many(matrix_set2, int(sys.argv[6]), int(sys.argv[7]))

#write_to_file(sys.argv[2], matrix_set1) #percent
#write_to_file(sys.argv[3], matrix_set2) # 1 - percent


#print("[FILE]: {} [Percent]: {}".format(sys.argv[1], 1))
#print_matrix(matrix_set1)
#print_matrix(matrix_set2)
#print("[FILE]: {} [Percent]: {}".format(sys.argv[2], int(sys.argv[5])/100))
#print_matrix(matrix_set1)
#print("[FILE]: {} [Percent]: {}".format(sys.argv[3], 1 - int(sys.argv[5])/100))
#print_matrix(matrix_set2)
