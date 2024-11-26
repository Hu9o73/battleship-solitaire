def parse_battleship_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()                    # Reading the file at given filepat
        
    lines = [line.strip() for line in lines]        # Strip newline characters and whitespaces (security measure)

    horizontal_numbers = list(map(int, lines[1]))   # Getting constraints
    vertical_numbers = list(map(int, lines[0]))
    ship_counts = list(map(int, lines[2]))

    grid = [list(line) for line in lines[3:]]       # Parsing the grid
    
    return horizontal_numbers, vertical_numbers, ship_counts, grid