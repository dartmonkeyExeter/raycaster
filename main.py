import pygame, math, debug

# pygame init
pygame.init()

# screen
# draw grid left side, game on right
window_width = 500
window_height = 350

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Raycaster")
fps = 60
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)

map = [ "111111111100000",
        "100000000111111",
        "111000111110001",
        "100000100000001",
        "101100000110001",
        "101000100111111",
        "111111111100000"]

height = len(map)
width = len(map[0])

# player
player_x = 250
player_y = 200
player_rot = 0
speed = 2.5
ray_length = 100
fov = 70
ray_step = 1  # how many pixels to move along each step in the raycasting process
space_multiplier = 8

walls = []
rays = []

for y in range(height):
    for x in range(width):
        if map[y][x] == "1":
            walls.append(pygame.Rect(x * 50, y * 50, 50, 50))

def cast_ray(ray_rot):
    ray_dx = math.cos(math.radians(ray_rot)) * ray_step
    ray_dy = math.sin(math.radians(ray_rot)) * ray_step
    
    current_x = player_x
    current_y = player_y
    
    while 0 <= current_x < (width * 50) and 0 <= current_y < (height * 50):  # boundary checks for the map size
        grid_x = int(current_x // 50)
        grid_y = int(current_y // 50)
        
        # Check if the current grid cell is a wall (denoted by "1")
        if map[grid_y][grid_x] == "1":
            # Found a wall, return the distance to the hit point
            return "Wall", math.sqrt((current_x - player_x)**2 + (current_y - player_y)**2)
        
        # Step along the ray path
        current_x += ray_dx
        current_y += ray_dy
    
    return None, None  # no hit, ray went out of bounds

# Example dynamic objects (items, enemies, etc.)
# This can be extended to include actual game objects with positions

def col_checks():
    wall_locs = []
    hitbox_width, hitbox_height = 6, 6  # Player's hitbox size
    
    # Define the four points (left, right, up, down) around the player
    points = [
        (player_x - hitbox_width // 2, player_y),  # Left
        (player_x + hitbox_width // 2, player_y),  # Right
        (player_x, player_y - hitbox_height // 2), # Up
        (player_x, player_y + hitbox_height // 2)  # Down
    ]

    # Check collision at each of the four points
    for point in points:
        # Create a small rectangle around the point to check for collisions
        player_rect = pygame.Rect(point[0] - 5, point[1] - 5, 10, 10)
        for wall in walls:
            if wall.colliderect(player_rect):  # Check if there's a collision
                # Check which direction the player is colliding with
                if point == points[0]:  # Left
                    wall_locs.append("left")
                elif point == points[1]:  # Right
                    wall_locs.append("right")
                elif point == points[2]:  # Up
                    wall_locs.append("up")
                elif point == points[3]:  # Down
                    wall_locs.append("down")

    return wall_locs

def renderer():
    # (actual slice height / distance) * distance to projection plane
    # slice height = 50
    # distance to projection plane = 500
    # distance = distance to wall (the rays)

    for i in range(fov):
        ray_rot = player_rot - (fov // 2) + i
        type_hit, distance = cast_ray(ray_rot)

        if distance is not None:

            ray_dx = distance * math.cos(math.radians(ray_rot))
            ray_dy = distance * math.sin(math.radians(ray_rot))

            if type_hit == "Wall":
                # Calculate the height of the wall slice
                slice_height = 50 / distance * 500
                # Calculate the top and bottom of the wall slice
                slice_top = 175 - slice_height // 2
                slice_bottom = 175 + slice_height // 2
                # Draw the wall slice


                pygame.draw.line(screen, value_to_gray(distance, 50), ((i*space_multiplier), slice_top), ((i*space_multiplier), slice_bottom), 8)
            
            elif type_hit == "Orb":
                slice_height = 20 / distance * 500
                # Calculate the top and bottom of the wall slice
                slice_top = 175 - slice_height // 2
                slice_bottom = 175 + slice_height // 2
                # Draw the wall slice


                pygame.draw.line(screen, RED, ((i*space_multiplier), slice_top), ((i*space_multiplier), slice_bottom), 2)
    

def value_to_gray(x, offset=0):
    # Ensure x is between 1 and 100
    x = max(1, min(100, x))
    
    # Map x from the range [1, 100] to [255, 0] (reverse the logic)
    gray_value = int(255 - ((x - 1) * 255 / 99))  # Reverse the formula
    
    # Apply offset to increase or decrease the gray value, ensuring it stays within [0, 255]
    gray_value = max(0, min(255, gray_value + offset))
    
    # Return the RGB tuple for the gray color
    return (gray_value, gray_value, gray_value)

def lock_mouse():
    pygame.mouse.set_visible(False)  # Hide the mouse cursor
    pygame.mouse.set_pos(window_width // 2, window_height // 2)  # Move cursor to center
    pygame.event.set_grab(True)  # Lock the mouse to the window

running = True

lock_mouse()

while running:
    screen.fill(BLACK)
    renderer()

    pygame.display.flip()

    # this only happens when we're kinda stuck in the wall, so we need to be pushed out
    if len(col_checks()) > 2:
        if "left" in col_checks():
            player_x += 5
        if "right" in col_checks():
            player_x -= 5
        if "up" in col_checks():
            player_y += 5
        if "down" in col_checks():
            player_y -= 5


    if pygame.key.get_pressed()[pygame.K_w]:
        dx = int(speed * math.cos(math.radians(player_rot)))
        dy = int(speed * math.sin(math.radians(player_rot)))
        if "right" in col_checks() and dx > 0:
            dx = 0
        if "left" in col_checks() and dx < 0:
            dx = 0
        if "up" in col_checks() and dy < 0:
            dy = 0
        if "down" in col_checks() and dy > 0:
            dy = 0
        
        player_x += dx
        player_y += dy

    if pygame.key.get_pressed()[pygame.K_s]:
        dx = int(speed * math.cos(math.radians(player_rot)))
        dy = int(speed * math.sin(math.radians(player_rot)))
        if "right" in col_checks() and dx < 0:
            dx = 0
        if "left" in col_checks() and dx > 0:
            dx = 0
        if "up" in col_checks() and dy > 0:
            dy = 0
        if "down" in col_checks() and dy < 0:
            dy = 0
        
        player_x -= dx
        player_y -= dy

    if pygame.key.get_pressed()[pygame.K_a]:
        dx = int(speed * math.cos(math.radians(player_rot - 90)))
        dy = int(speed * math.sin(math.radians(player_rot - 90)))
        if "right" in col_checks() and dx > 0:
            dx = 0
        if "left" in col_checks() and dx < 0:
            dx = 0
        if "up" in col_checks() and dy < 0:
            dy = 0
        if "down" in col_checks() and dy > 0:
            dy = 0
        
        player_x += dx
        player_y += dy

    if pygame.key.get_pressed()[pygame.K_d]:
        dx = int(speed * math.cos(math.radians(player_rot - 90)))
        dy = int(speed * math.sin(math.radians(player_rot - 90)))
        if "right" in col_checks() and dx < 0:
            dx = 0
        if "left" in col_checks() and dx > 0:
            dx = 0
        if "up" in col_checks() and dy > 0:
            dy = 0
        if "down" in col_checks() and dy < 0:
            dy = 0
        
        player_x -= dx
        player_y -= dy

    mouse_move = pygame.mouse.get_rel()
    
    player_rot += mouse_move[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False

    clock.tick(fps)
