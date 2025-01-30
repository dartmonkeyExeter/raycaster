# aaron's raycaster
import pygame, math

# pygame init
pygame.init()

# screen
screen = pygame.display.set_mode((500, 350))
pygame.display.set_caption("Raycaster")
fps = 60
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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

def draw_map():
    for y in range(7):
        for x in range(10):
            if map[y][x] == "1":
                pygame.draw.rect(screen, (255, 255, 255), (x * 50, y * 50, 50, 50))

def draw_player():
    pygame.draw.circle(screen, RED, (player_x, player_y), 5)
    pygame.draw.line(screen, WHITE, (player_x, player_y), (player_x + (20 * math.cos(math.radians(player_rot))), player_y + (20 * math.sin(math.radians(player_rot)))), 2)

    for i in range(fov):
        # for now we'll just draw the rays
        ray_rot = player_rot - (fov / 2) + i
        ray_dx = ray_length * math.cos(math.radians(ray_rot))
        ray_dy = ray_length * math.sin(math.radians(ray_rot))
        ray_x = player_x + ray_dx
        ray_y = player_y + ray_dy

        # draw the ray
        #pygame.draw.line(screen, WHITE, (player_x, player_y), (ray_x, ray_y), 2)

        # bresenham
        points = bresenham(player_x, player_y, int(ray_x), int(ray_y))
        for point in points:
            pygame.draw.circle(screen, RED, point, 2)
        

def bresenham(x1, y1, x2, y2):
    points = []
    
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    # Step 1: Handle the case when the line is vertical
    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1
        for y in range(y1, y2+1):
            points.append((x1, y))
        return points

    # Step 2: Handle the general case for non-vertical lines
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points
    

running = True

while running:
    screen.fill(BLACK)
    draw_map()
    draw_player()
    pygame.display.flip()

    if pygame.key.get_pressed()[pygame.K_UP]:
        dx = speed * math.cos(math.radians(player_rot))
        dy = speed * math.sin(math.radians(player_rot))
        player_x += dx
        player_y += dy

    if pygame.key.get_pressed()[pygame.K_DOWN]:
        dx = speed * math.cos(math.radians(player_rot))
        dy = speed * math.sin(math.radians(player_rot))
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
