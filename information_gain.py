import math

test = [
['0', 'Sunny', 'Hot', '222', 'Weak', 'No'],
['1', 'Sunny', 'Hot', '54', 'Strong', 'No'],
['2', 'Overcast', 'Hot', '12', 'Weak', 'Yes'],
['3', 'Rain', 'Mild', '43', 'Weak', 'Yes'],
['4', 'Rain', 'Cool', '54', 'Weak', 'Yes'],
['5', 'Rain', 'Cool', '234', 'Strong', 'No'],
['6', 'Overcast', 'Cool', '23', 'Strong', 'Yes'],
['7', 'Sunny', 'Mild', '13', 'Weak', 'No'],
['8', 'Sunny', 'Cool', '13', 'Weak', 'Yes'],
['9', 'Rain', 'Mild', '-4', 'Weak', 'Yes'],
['10', 'Sunny', 'Mild', '-2', 'Strong', 'Yes'],
['11', 'Overcast', 'Mild', '32', 'Strong', 'Yes'],
['12', 'Overcast', 'Hot', '2', 'Weak', 'Yes'],
['13', 'Rain', 'Mild', '1', 'Strong', 'No']
]
#This function determines if an attribute is composed of descrete or continuous data returning true if float or false if not
def float_test(arbitrary_column):

    try:
        float(arbitrary_column[0])
    except ValueError:
        return False
    else:
        return True
#######################################################################################################################################

# This function selects an attribute from the training set and separates it into a list of the attribute instances and a list containing the qualities of that attribute
def attribute_grab(matrix, column_index):
    
    attribute_list = []
    attribute_qualities = []

    # Loop transfers attribute data into a list
    for i in matrix:
        attribute_list.append(i[column_index])
    
    #Loop Creates list of attribute qualities by comparing remaining qualities with the qualities contained within the new list
    for i in attribute_list:
        if (attribute_qualities.count(i) == 0):
            attribute_qualities.append(i)

    return attribute_list, attribute_qualities
#######################################################################################################################################

#This function takes an attribute column and the target column, pairs them together then orders them from smallest to greatest returning an ordered_couple
def make_ordered_couple(numeric_list,target_list):

    coupled_list = []
    coupled_list.append(numeric_list)
    coupled_list.append(target_list)

    i = 0
    while (i < len(coupled_list[0])):

        count = 0
        while(count < len(coupled_list[0])):

            if((count + 1) >= len(coupled_list[0])):
                break

            elif(float(coupled_list[0][count]) == float(coupled_list[0][count + 1])):
                count +=1

            elif(float(coupled_list[0][count]) < float(coupled_list[0][count + 1])):
                count +=1

            else:
                holder = coupled_list[0][count] #Higher value in comparison set to holder
                coupled_list[0][count] = coupled_list[0][count + 1] # lower number value moved into lower index
                coupled_list[0][count + 1] = holder # Higher value number stored in higher index
                
                hand = coupled_list[1][count] #Higher value in comparison set to holder
                coupled_list[1][count] = coupled_list[1][count + 1] # lower number value moved into lower index
                coupled_list[1][count + 1] = hand # Higher value number stored in higher index

        i += 1      
    return coupled_list
#######################################################################################################################################

#This function takes an ordered couple and outputs the best split for that attribute
def make_splits(ordered_couple):
    
    splits = []
    i = 0
    while (i < len(ordered_couple[0])):
        if((i + 1) >= len(ordered_couple[0])):
            break
        else:
            splits.append(( (float(ordered_couple[0][i]) + float(ordered_couple[0][i + 1])) /2))
            i += 1
    return splits
#######################################################################################################################################

#This function returns two lists, that represent the elements below and above a specified split
def bi_split(ordered_couple, split_value):

    lower_list = []
    upper_list = []

    i = 0
    while(i < len(ordered_couple[0])):

        if(float(split_value) < float(ordered_couple[0][i])):

            upper_list.append(ordered_couple[0][i:])
            upper_list.append(ordered_couple[1][i:])

            lower_list.append(ordered_couple[0][:i])
            lower_list.append(ordered_couple[1][:i])
                        
            return lower_list, upper_list
                        
        i += 1 
#######################################################################################################################################

# This function calculates the entropys below and above a specified split value
def calc_split_sub_entropys(ordered_couple,split,target_qualities_list):

    low_up_entropys = []
    cont_sub_entropy_low = 0
    cont_sub_entropy_up = 0
    lower_target_list = bi_split(ordered_couple,split)[0][1] #assigns the list of targets under a given split
    upper_target_list = bi_split(ordered_couple,split)[1][1] #assigns the list of targets above a given split

    for i in target_qualities_list:

        if(float((lower_target_list).count(i)) == 0):
            cont_sub_entropy_low -= 0
            cont_sub_entropy_up -=  (upper_target_list).count(i)/ len(upper_target_list) * math.log((upper_target_list).count(i)/ len(upper_target_list),2)

        elif (float((upper_target_list).count(i)) == 0):
            cont_sub_entropy_up -= 0
            cont_sub_entropy_low -= (lower_target_list).count(i)/ len(lower_target_list) * math.log((lower_target_list).count(i)/ len(lower_target_list),2)

        else: 
            cont_sub_entropy_low -= (lower_target_list).count(i)/ len(lower_target_list) * math.log((lower_target_list).count(i)/ len(lower_target_list),2)
            cont_sub_entropy_up -=  (upper_target_list).count(i)/ len(upper_target_list) * math.log((upper_target_list).count(i)/ len(upper_target_list),2)
    
    low_up_entropys.append(cont_sub_entropy_low)
    low_up_entropys.append(cont_sub_entropy_up)

    return low_up_entropys
#######################################################################################################################################

#This function calculates entropy for a discrete set of targets and returns the overall entropy for total targets (assuming target variables are not continuous)
def calc_target_entropy(target_list,target_qualities):

    entropy_targets = 0
    i = 0
    while(i < len(target_qualities)): #Loop goes through the different attibute qualities (ie. sunny, rain, cloudy) and sums the overall entropy
    
        entropy_targets += -(target_list.count(target_qualities[i])/len(target_list))*math.log((target_list.count(target_qualities[i]))/len(target_list),2)
        i += 1

    return entropy_targets 
#######################################################################################################################################

#This function evaluates all possible splits and returns the information gain related to the best split
def calc_best_split(ordered_couple,target_qualities_list):
    
    IG = []
    in_gain = 0
    splits = make_splits(ordered_couple)
    
    for i in splits:
        enies = calc_split_sub_entropys(ordered_couple,i,target_qualities_list)
        in_gain = calc_target_entropy(ordered_couple[1],target_qualities_list) - ((len(bi_split(ordered_couple,i)[0][0]) / len(ordered_couple[0])) * enies[0] + (len(bi_split(ordered_couple,i)[1][0]) / len(ordered_couple[0])) * enies[1])

        IG.append(in_gain)

    return max(IG), IG
#######################################################################################################################################

#This function returns the best split value for a given continuous attribute
def value_of_best_split(matrix,continous_column_index):

    continuous_attribute = attribute_grab(matrix,continous_column_index)
    target_list = attribute_grab(matrix, len(matrix[0]) - 1)
    ord_couple = make_ordered_couple(continuous_attribute[0],target_list[0])
    splits = make_splits(ord_couple)
    IG_list_of_splits = calc_best_split(ord_couple,target_list[1])[1]
    best_split_index = IG_list_of_splits.index(calc_best_split(ord_couple,target_list[1])[0])
    
    value_of_split = splits[best_split_index]

    return value_of_split
#######################################################################################################################################

# This function calculates the entropy of an attribute quality and returns the value (entropy of sunny or rain)
def sub_entropy(attribute_couple, target_couple,indexer):

    #The dex_list is a 2D list whose length is the number of attribute qualities
    dex_list = make_att_spec_targ_list(attribute_couple,target_couple)

    sub_ent = 0
    i = 0
    while(i < len(target_couple[1])):
        # Logical statement to avoid log(0) domain error
        if (float(dex_list[indexer].count(target_couple[1][i]) == 0)):
            sub_ent -= 0
        else:
            sub_ent -= (float(dex_list[indexer].count(target_couple[1][i])/len(dex_list[indexer]))) * math.log(float(dex_list[indexer].count(target_couple[1][i]))/len(dex_list[indexer]), 2)
        i += 1

    return sub_ent

#This function creates a 2D list where the each sub-list contains the target classification for an attribute quality and returns it
def make_att_spec_targ_list(attribute_couple,target_couple):
    #The for and while loop directly below create a 2D list of index locations, each sub-list contains the index locations of that attribute quality (ie. sunny)
    index_loc_list = []
    for quality in attribute_couple[1]:
        sub_index_loc_list = []
        i = 0
        while(i < len(attribute_couple[0])):
            if(quality == attribute_couple[0][i]):
                sub_index_loc_list.append(i)
            i += 1
        index_loc_list.append(sub_index_loc_list)

    #The loops below use the attribute specific index locations from above to make a 2D list of target classifications specific to each attribute
    targets_wrt_spec_att = []
    i = 0
    while(i < len(index_loc_list)):
        sub_target_spc_att = []
        for item in index_loc_list[i]:
            sub_target_spc_att.append(target_couple[0][item])

        targets_wrt_spec_att.append(sub_target_spc_att)
        i += 1

    return targets_wrt_spec_att 
#######################################################################################################################################

#This function calculates the information gain of a specific data set attribute
def Information_Gain(matrix, column_index):
    
    info_gain = 0
    attribute_list_n_qual = []
    target_list_n_qual = []

    #Formation of Attribute 2D list containing attribute column and attribute qualities
    attribute_list_n_qual.append(attribute_grab(matrix, column_index)[0])
    attribute_list_n_qual.append(attribute_grab(matrix, column_index)[1])

    #Formation of target 2D list containing attribute column and target qualities
    target_list_n_qual.append(attribute_grab(matrix, (len(matrix[0]) - 1) )[0])
    target_list_n_qual.append(attribute_grab(matrix, (len(matrix[0]) - 1) )[1])

    if (float_test(attribute_list_n_qual[0])):

        ordered_couple = make_ordered_couple(attribute_list_n_qual[0],target_list_n_qual[0])
        info_gain = calc_best_split(ordered_couple,target_list_n_qual[1])[0]

        return info_gain

    else:
        Hsv_sum = 0
        i = 0
        #Iterates for the number of attribute qualities
        while(i < len(attribute_list_n_qual[1])):
            
            Hsv_sum += (attribute_list_n_qual[0].count(attribute_list_n_qual[1][i])/len(attribute_list_n_qual[0])) * sub_entropy(attribute_list_n_qual,target_list_n_qual,i)
            i += 1

        info_gain =  calc_target_entropy(target_list_n_qual[0],target_list_n_qual[1]) - Hsv_sum
        return info_gain
#######################################################################################################################################

#print(Information_Gain(test,1))
#print(Information_Gain(test,2))
#print(Information_Gain(test,3))
#print(Information_Gain(test,4))
#
#print(value_of_best_split(test,3))
