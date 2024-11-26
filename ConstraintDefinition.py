from GridSystem import *
from typing import List,Tuple

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


def find_boat(grid: List[List[any]], x: int, y: int, visited: set) -> List[Tuple[int, int]]:
    '''
    Finds all parts of a boat starting from (x, y) and ensures it's in one direction.
    '''
    boat = []
    stack = [(x, y)]
    direction = None  # To store the direction of the boat ('horizontal' or 'vertical')
    
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) not in visited:
            visited.add((cx, cy))
            boat.append((cx, cy))
            for nx, ny in get_neighbors(cx, cy, len(grid), len(grid[0])):
                if grid[ny][nx].state in ['M','<','>','v','^','S'] and (nx, ny) not in visited:
                    if direction is None:
                        # Determine initial direction
                        if nx == cx:
                            direction = 'vertical'
                        elif ny == cy:
                            direction = 'horizontal'
                    
                    # Ensure the current tile is in the same direction
                    elif (direction == 'vertical' and nx != cx) or (direction == 'horizontal' and ny != cy):
                        continue
                    
                    stack.append((nx, ny))
    return boat

def surroundedByWater(grid: List[List[any]]) -> bool:
    '''
    Check if all the boats inside of the grid passed as parameter are surrounded by water.
    '''
    rows, cols = len(grid), len(grid[0])
    visited = set()

    for y in range(rows):
        for x in range(cols):
            if grid[y][x].state in ['M','S','<','>','^','v'] and (x, y) not in visited:
                # Found a new boat, let's collect its coordinates
                boat = find_boat(grid, x, y, visited)

                # Check surrounding of the boat
                for bx, by in boat:
                    for dy in range(-1, 2):
                        for dx in range (-1, 2):
                            nx, ny = bx + dx, by + dy
                            # Skip out-of-bound indices and the boat's own position
                            if (dx == 0 and dy == 0) or not (0 <= ny < rows and 0 <= nx < cols):
                                continue
                            else:
                                if (grid[ny][nx].state != '.' and grid[ny][nx].state != '0') and (tuple([nx,ny]) not in boat):
                                    return False                       
    return True


def get_all_ships(grid: List[List[any]]) -> List[List[Tuple[int, int]]]:
    '''
    Finds all ships in the grid and returns them as a list of boats (each boat is a list of coordinates).
    '''
    visited = set()  # To keep track of visited cells
    ships = []  # To store all the boats

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x].state in ['M','<','>','^','v','S'] and (x, y) not in visited:
                # Find a new boat starting from (x, y)
                boat = find_boat(grid, x, y, visited)
                ships.append(boat)

    return ships


def shipCounter(shipsAndGrid: List[any]):
    '''
    Counts the number of ships inside of the grid.
    shipsAndGrid is an array with\n
    rank 0 being an array containing the target value for each ship type\n
    rank 1 the grid\n
    rank 2 the function stating if the grid is "finished" (= all variables have a state)\n
    The function returns False if the grid is finished but the number of ships per category don't correspond to the target.\n
    True otherwise.
    '''
    ships, grid, finished_func = shipsAndGrid[0], shipsAndGrid[1], shipsAndGrid[2]
    finished = finished_func()
    shipList = get_all_ships(grid)

    targetSub, targetDestroyer, targetCruiser, targetBattleship = ships[0], ships[1], ships[2], ships[3]
    subs, destroyers, cruisers, battleships = 0, 0, 0, 0
    
    for ship in shipList:
        if len(ship) == 1:
            subs += 1
        elif len(ship) == 2:
            destroyers += 1
        elif len(ship) == 3:
            cruisers += 1
        elif len(ship) == 4:
            battleships += 1
    
    if finished == True and (destroyers != targetDestroyer or subs != targetSub or cruisers != targetCruiser or battleships != targetBattleship):
        return False
    else:
        return True


def stateConstraint(dataArray):
    '''
    Function to represent the constraints on the state of each variable.\n
    Used to check if each tile is surrounded by admissible tiles.\n
    For instance, a "<" tile can't be followed by another "<" tile.
    '''
    var = dataArray[0]
    grid = dataArray[1]
    __, ___, y, x = var.name.split("_")     # Extract coordinates from variable name. Split on "_". Variables formated as VAR_NAME_ROW_COL
    x, y = int(x), int(y)               # Turn the row and col values to integers 
    surrounding = getSurroundingTiles(grid, x, y)
    
    if var.state == 'M':
        if surrounding[1][0]:
            if surrounding[1][0].state not in ['M', '<']:
                #print("False_1_0")
                return False
            else:
                if not surrounding[1][2] and surrounding[1][0].state in ['M','<']:
                    #print("False_1_0_B")
                    return False
        else:
            if surrounding[0][1] and surrounding[0][1].state == '.':
                return False

        if surrounding[0][1]:
            if surrounding[0][1].state not in ['M','^','0','.']:
                #print("False_0_1")
                return False
            else:
                if not surrounding[2][1] and surrounding[0][1].state in ['M','^']:
                    #print("False_0_1_B")
                    return False
        if surrounding[2][1]:
            if surrounding[2][1].state not in ['M','v', '0', '.']:
                #print("False_2_1")
                return False
            else:
                if not surrounding[0][1] and surrounding[2][1].state in ['M','v']:
                    #print("False_2_1_B")
                    return False
        if surrounding[1][2]:
            if surrounding[1][2].state not in ['M', '>', '0', '.']:
                #print("False_1_2")
                return False
            else:
                if not surrounding[1][0] and surrounding[1][2].state in ['M','>']:
                    #print("False_1_2_B")
                    return False

        return True
    
    elif var.state == 'v':
        if surrounding[0][1]:
            if surrounding[0][1].state in ['M', '^', '0']:
                if surrounding[2][1]:
                    if surrounding[2][1].state in ['.', '0']:
                        return True

        
    elif var.state == '^':
        if surrounding[2][1]:
            if surrounding[2][1].state in ['M', 'v', '0']:
                if surrounding[0][1]:
                    if surrounding[0][1].state in ['.', '0']:
                        return True

        
    elif var.state == '>':
        if surrounding[1][0]:
            if surrounding[1][0].state in ['M', '<']:
                if surrounding[1][2]:
                    if surrounding[1][2].state in ['.','0']:
                        return True
                    else:
                        return False
                else:
                    return True

    elif var.state == '<':
        if surrounding[1][2]:
            if surrounding[1][2].state in ['M', '>', '0']:
                if surrounding[1][0]:
                    if surrounding[1][0].state in ['.','0']:
                        return True
                    else:
                        return False
                else:
                    return True
            else:   
                return False
        else:
            return False

        
    elif var.state == 'S':
        for a in range(3):
            for b in range(3):
                if not (a==1 and b==1):
                    if surrounding[a][b] and surrounding[a][b].state not in ['0','.']:
                        return False

        return True
    
    elif var.state == '.':
        if surrounding[0][1]:
            if surrounding[0][1].state in ['^']:
                return False
        if surrounding[2][1]:
            if surrounding[2][1].state in ['v']:
                return False
        if surrounding[1][0]:
            if surrounding[1][0].state in ['<']:
                return False
        if surrounding[1][2]:
            if surrounding[1][2].state in ['>']:
                return False
        if surrounding[1][0] and surrounding[1][0].state in ['M'] and surrounding[0][0] and surrounding[0][0].state in ['.']:
            return False
        if surrounding[0][1] and surrounding[0][1].state in ['M'] and surrounding[0][2] and surrounding[0][2].state in ['.']:
            return False
        return True     
    else:
        return True
    
    return False