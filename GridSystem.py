from typing import List

def printGrid(grid: List[List[any]]):
    '''
    Simply prints a matrix passed as a parameter.
    '''
    for row in grid:
        for col in row:
            print(col, end= " ")
        print("")


def printBsGrid(bsGrid:List[List[any]], vertical:List[any], horizontal:List[any]):
    '''
    Printing a grid, alongside its veritcal and horizontal constraints.
    '''
    print("", end="  ")
    for val in vertical:
        print(val, end=" ")
    print()

    counter = 0
    for row in bsGrid:
        print(horizontal[counter], end= " ")
        for col in row:
            print(col, end =" ")
        print()
        counter+=1


def getSurroundingTiles(matrix: List[List[any]], x: int, y: int) -> List[List[any]]:
    """
    Given a 2D matrix and coordinates (x, y), return a 3x3 matrix representing
    the tile at (x, y) and its surrounding tiles. Tiles outside the matrix bounds are None.
    """
    rows, cols = len(matrix), len(matrix[0])
    
    # Initialize 3x3 surrounding tiles with None
    surroundingTiles = [[None for _ in range(3)] for _ in range(3)]

    # Iterate through the 3x3 grid centered around (x, y)
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy  # Calculate the neighbor's coordinates
            if 0 <= nx < cols and 0 <= ny < rows:  # Check if within bounds
                surroundingTiles[dy + 1][dx + 1] = matrix[ny][nx]
    
    return surroundingTiles