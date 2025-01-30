import pygame, math

# pygame init
pygame.init()

# screen
# draw grid left side, game on right
screen = pygame.display.set_mode((1000, 350))
pygame.display.set_caption("Raycaster")
fps = 60
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)

map = ["1111111111",
        "1000000001",
        "1000000001",
        "1000000001",
        "1000000001",
        "1000000001",
        "1111111111"]

# player
player_x = 250
player_y = 175
player_rot = 0
speed = 5
ray_length = 100
fov = 70
ray_step = 1  # how many pixels to move along each step in the raycasting process

walls = []
rays = []

for y in range(7):
    for x in range(10):
        if map[y][x] == "1":
            walls.append(pygame.Rect(x * 50, y * 50, 50, 50))

def draw_map():
    for y in range(7):
        for x in range(10):
            if map[y][x] == "1":
                pygame.draw.rect(screen, (255, 255, 255), (x * 50, y * 50, 50, 50))

def draw_player():
    pygame.draw.circle(screen, RED, (player_x, player_y), 5)
    pygame.draw.line(screen, WHITE, (player_x, player_y), (player_x + (20 * math.cos(math.radians(player_rot))), player_y + (20 * math.sin(math.radians(player_rot)))), 2)

def cast_ray(ray_rot):
    ray_dx = math.cos(math.radians(ray_rot)) * ray_step
    ray_dy = math.sin(math.radians(ray_rot)) * ray_step
    
    current_x = player_x
    current_y = player_y
    
    while 0 <= current_x < 500 and 0 <= current_y < 350:  # boundary checks for the map size
        grid_x = int(current_x // 50)
        grid_y = int(current_y // 50)
        
        # Check if the current grid cell is a wall (denoted by "1")
        if map[grid_y][grid_x] == "1":
            # Found a wall, return the distance to the hit point
            return math.sqrt((current_x - player_x)**2 + (current_y - player_y)**2)
        
        # Step along the ray path
        current_x += ray_dx
        current_y += ray_dy
    
    return None  # no hit, ray went out of bounds

def render_rays():
    for i in range(fov):
        # For now, just cast the rays and render them
        ray_rot = player_rot - (fov // 2) + i
        distance = cast_ray(ray_rot)
        if distance:
            ray_dx = distance * math.cos(math.radians(ray_rot))
            ray_dy = distance * math.sin(math.radians(ray_rot))
            ray_end_x = player_x + ray_dx
            ray_end_y = player_y + ray_dy
            pygame.draw.line(screen, RED, (player_x, player_y), (ray_end_x, ray_end_y), 1)

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
        distance = cast_ray(ray_rot)
        if distance:
            ray_dx = distance * math.cos(math.radians(ray_rot))
            ray_dy = distance * math.sin(math.radians(ray_rot))
            ray_end_x = player_x + ray_dx
            ray_end_y = player_y + ray_dy
            
            # Calculate the height of the wall slice
            slice_height = 50 / distance * 500
            # Calculate the top and bottom of the wall slice
            slice_top = 175 - slice_height // 2
            slice_bottom = 175 + slice_height // 2
            # Draw the wall slice
            pygame.draw.line(screen, RED, (500 + i, slice_top), (500 + i, slice_bottom), 1)

running = True

while running:
    screen.fill(BLACK)
    draw_map()
    render_rays()  # Render all the rays
    renderer()
    draw_player()
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


    if pygame.key.get_pressed()[pygame.K_UP]:
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

    if pygame.key.get_pressed()[pygame.K_DOWN]:
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

    if pygame.key.get_pressed()[pygame.K_LEFT]:
        player_rot -= 5
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        player_rot += 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(fps)
