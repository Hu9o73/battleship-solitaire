# Required imports:
#   - Constraint functions
#   - Parsing input (to read input files)
from ConstraintDefinition import *
from ParsingInput import *

class Variable:
    '''Class used to define variables.'''
    def __init__(self, name, domain, state = None):
        self.name = "VAR_" + name           # Name of our constraint
        self.domain = list(domain)          # Values it can take
        self.state = state                  # Base state is None

    def __str__(self):
        return "Variable {} | State : {} | Domain : {}\n".format(self.name, self.state, self.domain)
    

    def setState(self, state):
        '''Function to set the state "properly". Verifying that the state passed as a parameter is in the domain.'''
        
        if state in self.domain or state == "0" or state == None:   # Check if state is in the domain, or 0, or None (for u)
            self.state = state                                      # Assign domain
            pass
        else:
            pass # Do nothing...
    


class Constraint:
    '''Class used t define constraints. Scope are variables related to this constraint.'''

    def __init__(self, name, scope, function = lambda: True):
        self.name = "CONS_" + name  # Name of our constraint
        self.scope = list(scope)    # Scope of the constraint => Variables related to our constraint
        self.function = function    # Assigning the bool function that states if our constraint is respected or not. If nothing specified, we return True no matter what

    def __str__(self):
        return self.name

    
    def check(self):
        '''Check if constraint is respected by applying its associted function to its scope
        (= the variables related to the constraint.)'''

        if self.function(self.scope) == False:
                return False
        
        return True 
    

class CSP:
    '''Base class for Constraint Satisfaction Problem declaration.'''

    def __init__(self, name, variables, constraints):
        self.name = "CSP_" + name       # Name of the problem
        self.variables = variables      # Variables of the problem
        self.constraints = constraints  # Constraints of the problem. Each constraint has variables related to it. Make sure they're included inthe variables list.

    def __str__(self):
        return self.name
    


def solutionGridBuilder(solution, rows=6, cols=6):
    '''Returns a matrix representing the grid of a solution. Solution is inputed as a dictionnary.'''

    matrix = [["" for _ in range(cols)] for _ in range(rows)]   # Create an "empty" row*col matrix.

    # Fill the matrix
    for var, value in solution.items():             # For all items in the solution dictionary (var, corresponding value)
        __, ___, row, col = var.name.split("_")     # Extract coordinates from variable name. Split on "_". Variables formated as VAR_NAME_ROW_COL
        row, col = int(row), int(col)               # Turn the row and col values to integers
        matrix[row][col] = value                    # Assign to the row/col coordinates the vaue.

    return matrix                                   # Return the matrix




def defineLineConstraints(bspb, gridVar, direction, label="Line"):
    '''
    Function to define a "linear constraint". Direction being horizontal or vertical.
    We build an array with the target value and a line's variables.
    GridVar is a matrix [[],[],[]]. Each array in the matrix is either a row or a column.
    We concatenate the target and the values and create a constraint on this array.
    The associated function is "isLineRespected". See its definition in ConstraintDefinition.py
    '''

    lineCount = 0                               # Count how many lines we dealt with yet
    for line in gridVar:                        # For every line in GridVar (= for every row or every col)
        array = []                              # Initialize an array
        array.append(direction[lineCount])      # We add the target value. Direction is an array where each value with id=i is the target variable of line n°i

        for value in line:                      # For every value in the line
            array.append(value)                 # We add this value to our array, thus after the target value

        cons = Constraint("{}_{}".format(label, lineCount), array, isLineRespected)   # We build a constraint based on this array, with function isLineRespected.
        bspb.constraints.append(cons)           # We add the constraint to the battleship CSP problem given as parameter
        lineCount +=1                           # We add one line to the final count




class BattleShipProblem(CSP):
    '''
    Class for Battleship problem definiton and solving.
    Based on the CSP class.
    '''

    def __init__(self, name, filepath):
        
        super().__init__(name=name, variables=[], constraints=[])               # Initialize the CSP class
        
        horizontal, vertical, ships, grid = parse_battleship_input(filepath)    # Get the grid, ships, target line values from the filepath, using the parse input function

        self.grid = grid                                                        # Defining the "grid" as an array
        self.gridVarRow = []                                                    # Initialize the gridVarRow, a matrix where each element is an array representing a row
        self.gridVarCol = []                                                    # Initialize the gridVarRow, a matrix where each element is an array representing a column
        #self.domain = ['0','.','S','<','>','M','^','v']
        self.domain = ['.','M']                                                 # Defining the domain. We only use M and . for efficiency purposes. Considering M tiles as ships, depending on where they are we can know what exact type it is (^,v,>,<,S)
        
        self.horizontal = horizontal                # Used to return these values if needed
        self.vertical = vertical                    # Used to return these values if needed

        # Defining gridVarRow and gridVarCol
        rowNum = 0
        colNum = 0       

        for row in grid:                            # For every row in the grid
            tempRow = []                            # Create a temporary row
            for column in row:                      # For every value in this row, thus every column
                var = Variable("Cell_{}_{}".format(rowNum, colNum), self.domain, column)    # We create a variable corresponding to that cell
                tempRow.append(var)                 # Add this variable to our temporary row
                self.variables.append(var)          # We add the variable to the variables array of our CSP problem

                colNum +=1                          # Column counter used to name variables
            
            self.gridVarRow.append(tempRow)         # We add the temporary row as an actual row in "gridVarRow"
            colNum = 0                              # Reset column counter (coming back to col 0)
            rowNum +=1                              # Passing to the next line, used to name the variables

        for i in range(len(self.gridVarRow[0])):        # For every column
            tempCol = []                                # We create a temp column
            for j in range(len(self.gridVarRow)):       # For every row in that column
                tempCol.append(self.gridVarRow[j][i])   # We add to our temp column its value (the variable)

            self.gridVarCol.append(tempCol)             # Once done, we add the full temp Column to the gridVarCol matrix


        # Setting the constraints
        defineLineConstraints(self, self.gridVarRow, horizontal, "ROW")     # Using defineLine function to set the row constraints
        defineLineConstraints(self, self.gridVarCol, vertical, "COL")       # Using defineLine function to set the col constraints
    

    def solve(self, method):
        '''
        To call different solvers.\n
        Available solvers :\n
            "backtracking"\n
        Returns solution (dictionary)
        '''
        if(method == "backtracking"):
            return self.backtracking_search()
        else:
            return None
        

    def backtracking_search(self, assignment = {}):
        '''
        Perform a backtracking search to solve the problem.
        If it finds a solution, its yielded as a dictionnary, where each variable of our problem has an associated state.
        '''
        return self.recursive_backtracking(assignment)  # Start backtracking recursion
        

    def recursive_backtracking(self, assignment):
        '''Recursive backtracking function.'''

        if self.is_complete(assignment):                    # If assignment is complete (all variables assignated + constraints validated)
            return assignment                               # We return the solution 

        var = self.select_unassigned_variable(assignment)   # (Else) We select and unassigned variable

        if not var:                                         # If we don't get a variable
            return None                                     # We return None, as no new variable is available

        for value in var.domain:                            # Otherwise, for every value in the variable's domain ( [., M] normally)
            if self.is_consistent(var, value):              # We check the consistency of our solution if we temporarily set the variable's state to the given value
                var.setState(value)                         # If it is, we set the variable's state to the given value
                assignment[var] = value                     # And add this change to our final solution

                result = self.recursive_backtracking(assignment)    # Recursion, to go on to the next variable

                if result is not None:                      # If the result is not None, means that a solution was found so we return it
                    return result

                # Backtrack                                  If we ever come back to this place, it means that result was None, meaning that no solution was found
                del assignment[var]                         # We delete the assignment in our solution
                var.setState(None)                          # And set the state back to None (or 0, which would mean unassigned)

        return None                                         # After having check all the possible value, if no solution was found we return None

    
    def printGrid(self):
        '''Printing the grid of the batleship problem. Prints the states of each variable in a human-readable grid format.'''

        for row in self.gridVarRow:             # For each row
            for value in row:                   # We check every value in the row
                print(value.state, end=" ")     # Print them on the same line
            print()                             # Print new line for every row
        print("-----------")                    # Print separator


    def select_unassigned_variable(self, assignment):
        '''Selects an unassigned variable, passing the assignment as a parameter to know what variables are assigned.
            Simply returns the next unassigned variable.'''
        
        for var in self.variables:          # For all variables
            if var not in assignment:       # If var is not assigned
                return var                  # We return it
            
        return None                         # Otherwise we return None


    def is_consistent(self, var, value):
        '''For the given variable, checks if setting its state to the value inputed as a parameter
            breaks the constraints the variable is related to.'''
        
        var.setState(value)                                 # Setting the state temporarily
        for cons in self.constraints:                       # For all constraints in the bs problem
            if var in cons.scope and not cons.check():      # If the variable is in its scope and breaks the constraints
                var.setState(None)                          # We set the state to None
                return False                                # And return false
        var.setState(None)                                  # Otherwise we reset the state
        return True                                         # But return true
    
    def is_complete(self, assignment):
        '''Check if all variables are assigned and all constraints are satisfied'''
        return len(assignment) == len(self.variables) and all(cons.check() for cons in self.constraints)
        
    
    