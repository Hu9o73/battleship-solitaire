def isLineRespected(array):
    '''
    Used to check if a line's target value is respected.
    The parameter should an array with:
    [0] = targetValue
    [:] = the row you're checking (i.e. [.,.,<,M,>,.])
    The function will then take the first value of the array you passed as parameter to check if the
    number of "ship tile" corresponds to the value in array[0]. 
    '''
    target = array[0]                                               # We get the target from the first value of our array
    count = 0                                                       # To count the "boats" in my line
    unassigned = 0                                                  # To count the unassigned values

    for var in array[1:]:                                           # For every variable in the array, from index 1 to the end
        if var.state in ['S', 'M', '<', '>', '^', 'v']:             # If the state is a valid ship parts
            count += 1                                              # We count 1 ship
        elif var.state == None or var.state == '0':                 # Else if the state is None or 0
            unassigned += 1                                         # We count an unassigned variable

    # We want to check that the boat count == the target
    # But if we simply put count == target, having 1 boat out of 3 (for example), will state that the condition isn't respected
    # And thus, that the solution isn't consistent forcing us to try another variable (because of how the script is made)
    #
    # To check consistency:
    # We return True if the count <= target and the count + unassigned values >= target
    # This way, the function will yield True if count == target (because unassigned would be 0) or if we still can place ships
    return count <= target and (count + unassigned) >= target


# Note : Completeness will be checked in an "is_complete" function, making sure the solution is consitent AND all variables are assigned.
