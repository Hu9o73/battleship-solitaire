def parse_battleship_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    # Strip newline characters and whitespaces
    lines = [line.strip() for line in lines]
    
    # Constraints
    horizontal_numbers = list(map(int, lines[1]))
    vertical_numbers = list(map(int, lines[0]))
    
    # Ship counts
    ship_counts = list(map(int, lines[2]))
    
    # Parse the 6x6 grid
    grid = [list(line) for line in lines[3:]]
    
    return horizontal_numbers, vertical_numbers, ship_counts, grid