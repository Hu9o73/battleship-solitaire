from PIL import Image, ImageDraw, ImageFont

icons_paths = {
    'S': 'Images/Assets/single_tile_ship_icon.png',
    '<': 'Images/Assets/left_arrow_icon.png',       
    '>': 'Images/Assets/right_arrow_icon.png',      
    'M': 'Images/Assets/center_part_icon.png',      
    '^': 'Images/Assets/up_arrow_icon.png',         
    'v': 'Images/Assets/down_arrow_icon.png',
    '.': 'Images/Assets/water_icon.png'     
}

def draw_battleship_grid(grid, icon_paths = icons_paths, filename = "output.png"):
    
    cell_size = 64                              # Define the size of a cell
    grid_width = len(grid[0]) * cell_size       # Getting the grid width
    grid_height = len(grid) * cell_size         # and height
    
    # Create a new blank image with white background
    img = Image.new('RGB', (grid_width, grid_height), color="white")
    draw = ImageDraw.Draw(img)

    # Load and resize icons based on the cell size. Icons are custom made on another software (photoshop) and then imported to the project file as .png
    icons = {}
    for key, path in icon_paths.items():
        try:
            icon = Image.open(path)
            icons[key] = icon.resize((cell_size, cell_size))        # We resize the png to match the size of a cell
        except FileNotFoundError:
            print(f"Warning: Icon for '{key}' not found at {path}, using text instead.")
    
    # Load a font for drawing text (used if the icon isn't loaded correctly)
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()


    # Draw the grid and its contents
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # Draw a rectangle for each cell (optional, just for gridlines)
            x0, y0 = col * cell_size, row * cell_size
            x1, y1 = (col + 1) * cell_size, (row + 1) * cell_size
            draw.rectangle([x0, y0, x1, y1], outline="black", width=2)

            # Get the symbol for the cell
            symbol = grid[row][col]

            # If the symbol corresponds to an icon, paste the icon in the cell
            if symbol in icons:
                icon = icons[symbol]
                img.paste(icon, (x0, y0))
            else:
                # If no icon, draw the symbol as text in the center of the cell
                text = str(symbol)
                # Get the bounding box of the text
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = x0 + (cell_size - text_width) / 2
                text_y = y0 + (cell_size - text_height) / 2
                draw.text((text_x, text_y), text, fill="black", font=font)

    img.save("Images/Assets/Outputs/" + filename)
    return img