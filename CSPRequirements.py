# Variable, Constraints and CSP base classes to implement a problem as a CSP
from ConstraintDefinition import *
from ParsingInput import *
from itertools import product
from baseChange import *
import numpy as np


class Variable:

    def __init__(self, name, domain, state = None):
        self.name = "VAR_" + name        # Name of our constraint
        self.domain = list(domain)    # Values it can take
        self.state = state
        self.originalDomain = list(domain)  # Keeping a copy of the originalDomain for later backtracking

    def __str__(self):
        return "Variable {} | State : {} | Domain : {}\n".format(self.name, self.state, self.domain)
    

    def setState(self, state):
        if state in self.domain or state == "0" or state == None:
            self.state = state
            pass
        else:
            pass # Do nothing...


    def remove_from_domain(self, value):
        if value in self.domain:
            self.domain.remove(value)

    def restore_domain(self):
        """ Restore the domain to its original state during backtracking. """
        self.domain = list(self.originalDomain)

    
    


class Constraint:

    def __init__(self, name, scope, function = lambda: True):
        self.name = "CONS_" + name            # Name of our constraint
        self.scope = list(scope)    # Scope of the constraint => Variables related to our constraint
        self.function = function    # Assigning the bool function that states if our constraint is respected or not. If nothing specified, we return True no matter what

    def __str__(self):
        return self.name

    
    def check(self):
        if self.function(self.scope) == False:
                return False
        
        return True 
    

class CSP:

    def __init__(self, name, variables, constraints):
        self.name = "CSP_" + name
        self.variables = variables
        self.constraints = constraints

    def __str__(self):
        return self.name
    


def solutionGridBuilder(solution, rows=6, cols=6):
    matrix = [["" for _ in range(cols)] for _ in range(rows)]

    # Fill the matrix
    for var, value in solution.items():
        # Extract coordinates from variable name
        __, ___, row, col = var.name.split("_")
        row, col = int(row), int(col)
        matrix[row][col] = value

    return matrix




def defineLineConstraints(bspb, gridVar, direction, label="Line"):
    lineCount = 0
    for line in gridVar:
        array = []
        array.append(direction[lineCount])

        for value in line:
            array.append(value)

        cons = Constraint("{}_{}".format(label, lineCount), array, isLineRespected)
        bspb.constraints.append(cons)
        lineCount +=1




class BattleShipProblem(CSP):

    def __init__(self, name, filepath):
        super().__init__(name=name, variables=[], constraints=[])
        
        horizontal, vertical, ships, grid = parse_battleship_input(filepath)

        self.grid = grid
        self.gridVarRow = []
        self.gridVarCol = []
        #self.domain = ['0','.','S','<','>','M','^','v']
        self.domain = ['.','M']
        

        # Defining gridVarRow and gridVarCol
        rowNum = 0
        colNum = 0       

        for row in grid:
            tempRow = []
            for column in row:
                var = Variable("Cell_{}_{}".format(rowNum, colNum), self.domain, column)
                tempRow.append(var)
                self.variables.append(var)

                colNum +=1
            
            self.gridVarRow.append(tempRow)
            colNum = 0
            rowNum +=1
        
        for i in range(len(self.gridVarRow[0])):
            tempCol = []
            for j in range(len(self.gridVarRow)):
                tempCol.append(self.gridVarRow[j][i])

            self.gridVarCol.append(tempCol)


        # Setting the constraints
        defineLineConstraints(self, self.gridVarRow, horizontal, "ROW")
        defineLineConstraints(self, self.gridVarCol, vertical, "COL")
    

    def backtracking_search(self, assignment = {}):
        return self.recursive_backtracking(assignment)
        



    def recursive_backtracking(self, assignment):
        self.printGrid()
        if self.is_complete(assignment):
            print("Assignment is complete !")
            return assignment

        print("Selecting variable...")
        var = self.select_unassigned_variable(assignment)
        print("Variable selected : ", var)

        if not var:
            print("Variable not valid")
            return None  # No unassigned variable found

        print("Starting loop...")
        for value in var.domain:
            print("Value selected : ", value)
            if self.is_consistent(var, value):
                print(f"BSP consistent. Trying {value} for {var.name}")  # Debugging
                var.setState(value)
                print("State set: ", var.state)
                assignment[var] = value
                print("Assignment set: ", assignment[var])

                result = self.recursive_backtracking(assignment)
                if result is not None:
                    print("Returning a not None result: ", result)
                    return result

                # Backtrack
                print(f"Backtracking on {var.name}")
                del assignment[var]
                var.setState("0")
                print("Backtracking... updated state: ", var.state)
                self.printGrid()

        print("Returning none...")
        return None

    
    

    def printGrid(self):
        for row in self.gridVarRow:
            for value in row:
                print(value.state, end=" ")
            print()

        print("-----------")


    def is_complete(self, assignment):
        # Check if all variables are assigned and all constraints are satisfied
        return len(assignment) == len(self.variables) and all(cons.check() for cons in self.constraints)
    

    def select_unassigned_variable(self, assignment):
        # First unassigned variable is chosen
        for var in self.variables:
            if var not in assignment:
                return var

        return None
    
    def is_consistent(self, var, value):
        var.setState(value)
        #print("TempVar : ", var)
        for cons in self.constraints:
            if var in cons.scope:
                print(cons)

            if var in cons.scope and not cons.check():
                var.setState(None)
                return False
        var.setState(None)
        return True
    
    