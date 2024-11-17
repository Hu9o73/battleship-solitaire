def isLineRespected(array):
    '''
    The parameter should an array with:
    [0] = targetValue
    [:] = the row you're checking (i.e. [.,.,<,M,>,.])
    The function will then take the first value of the array you passed as parameter to check if the
    number of "ship tile" corresponds to the value in array[0]. 
    '''
    target = array[0]
    count = 0
    unassigned = 0

    for var in array[1:]:
        #print(var.state, end="")
        if var.state in ['S', 'M', '<', '>', '^', 'v']:  # Valid ship parts
            count += 1
        elif var.state == None or var.state == '0':  # Unassigned cell
            unassigned += 1
    
    #print()
    #for val in array[1:]:
        #print("Name : ", val.name, " | state : ", val.state, end= " | ")
    
    #print("Count:", count, " | unassigned: ", unassigned, " | Target : ", target)
    # Constraint is satisfied if we can still potentially reach the target
    return count <= target and (count + unassigned) >= target