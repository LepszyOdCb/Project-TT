import pygame
import random

# Constants
run = True
map_size = 128
map_data = []
window_width = 1024 + 128 + 128 - 32
window_height = 960 + 32
cell_size = 32
max_cell_displayed = 32 - 1

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (255, 0, 255)

# Camera starts in center
cam_pos = [map_size // 4 + 1, map_size // 4 + 1]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("T1")
font = pygame.font.SysFont(None, 16)
clock = pygame.time.Clock()

# Map indexing
# 0 - empty
# 1 - city_center
# 2 - city_center_border
# 3 - road
# 4 - house

# Functions
def far_enough(x, y, cities, min_dist):
    for cx, cy in cities:
        if ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 < min_dist:
            return False
    return True

def house_gen(map, x, y):
    if map[x][y] == 3:
        for i in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if random.randint(0, 3) == 0 and map[x + i[0]][y + i[1]] == 0:
                map[x + i[0]][y + i[1]] = 4
    return map

def map_gen(size):
    map = [[0 for _ in range(size)] for _ in range(size)]
    cities_cords = []

    # Capital
    while True:
        x = random.randint((map_size // 2) - (map_size // 16), (map_size // 2) + (map_size // 16))
        y = random.randint((map_size // 2) - (map_size // 16), (map_size // 2) + (map_size // 16))
        if far_enough(x, y, cities_cords, 16):
            break

    cities_cords.append((x, y))

    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            map[x + i][y + j] = 2
    map[x - 1][y - 1] = 1

    map[x - 2][y - 2] = 3
    map[x - 2][y + 2] = 3
    map[x + 2][y - 2] = 3
    map[x + 2][y + 2] = 3
    map[x][y - 2] = 3
    map[x][y + 2] = 3
    map[x - 2][y] = 3
    map[x + 2][y] = 3
    map[x + 1][y - 2] = 3
    map[x - 1][y + 2] = 3
    map[x - 2][y + 1] = 3
    map[x + 2][y - 1] = 3
    map[x + 1][y + 2] = 3
    map[x - 1][y - 2] = 3
    map[x - 2][y - 1] = 3
    map[x + 2][y + 1] = 3

    map[x - 3][y - 2] = 3
    map[x - 2][y - 3] = 3
    map[x + 2][y - 3] = 3
    map[x + 3][y - 2] = 3
    map[x - 4][y - 2] = 3
    map[x + 4][y - 2] = 3
    map[x - 3][y + 2] = 3
    map[x + 3][y + 2] = 3
    
    map[x - 2][y + 3] = 3
    map[x + 2][y + 3] = 3
    map[x - 4][y + 2] = 3
    map[x + 4][y + 2] = 3
    map[x - 2][y - 4] = 3
    map[x + 2][y - 4] = 3

    
    
    # Cities
    for _ in range((size // 64) ** 2):
        while True:
            x = random.randint((map_size // 2) - (map_size // 8), (map_size // 2) + (map_size // 8))
            y = random.randint((map_size // 2) - (map_size // 8), (map_size // 2) + (map_size // 8))

            if far_enough(x, y, cities_cords, 9):
                break

        cities_cords.append((x, y))

        for i in (0, 1):
            for j in (0, 1):
                map[x + i][y + j] = 2
        map[x][y] = 1

        # Side choises
        # 1 - down right
        # 2 - right up down
        # 3 - left up
        # 4 - left up
        side = random.randint(1, 4)
        if side == 1:
            map[x + 1][y + 2] = 3
            map[x + 2][y + 1] = 3
            map[x + 2][y + 2] = 3
            map[x + 2][y] = 3
            map[x + 2][y - 1] = 3
            map[x + 2][y - 2] = 3
        elif side == 2:
            map[x + 2][y + 1] = 3
            map[x + 1][y + 2] = 3
            map[x][y + 2] = 3
            map[x - 1][y + 2] = 3
            map[x + 2][y + 2] = 3
            map[x - 1][y + 1] = 3
        elif side == 3:
            map[x][y - 1] = 3
            map[x - 1][y] = 3
            map[x - 1][y - 1] = 3
            map[x - 1][y - 1] = 3
            map[x - 1][y] = 3
            map[x - 1][y + 1] = 3
            map[x + 1][y - 1] = 3
        elif side == 4:
            map[x - 1][y - 1] = 3
            map[x - 0][y - 1] = 3
            map[x - 1][y - 1] = 3
            map[x + 1][y - 1] = 3
            map[x + 1][y - 1] = 3   
            map[x - 1][y] = 3
            map[x - 1][y + 1] = 3
            map[x - 1][y + 2] = 3

    # Vilages
    for _ in range((size // 32) ** 2):
        while True:
            x = random.randint(16, map_size - 15)
            y = random.randint(16, map_size - 15)

            if far_enough(x, y, cities_cords, 6):
                break

        cities_cords.append((x, y))
        map[x][y] = 1

        # Side choises
        # 1 - up
        # 2 - right
        # 3 - down
        # 4 - left

        side = random.randint(1, 4)
        if side == 1:
            for i in (-1, 0, 1):
                map[x - 1][y + i] = 3
        elif side == 2:
            for i in (-1, 0, 1):
                map[x + i][y + 1] = 3
        elif side == 3:
            for i in (-1, 0, 1):
                map[x + 1][y + i] = 3
        elif side == 4:
            for i in (-1, 0, 1):
                map[x + i][y - 1] = 3

    return map, cities_cords

# Initialize map
map_data, cities_cords = map_gen(map_size)
print(cities_cords)

for i in range(map_size):
    for j in range(map_size):
        if map_data[i][j] == 3:
            map_data = house_gen(map_data, i, j)

# Main loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Camera movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                cam_pos[1] -= 1
            if event.key == pygame.K_s:
                cam_pos[1] += 1
            if event.key == pygame.K_a:
                cam_pos[0] -= 1
            if event.key == pygame.K_d:
                cam_pos[0] += 1
        #if event.type == pygame.mouse.get_pressed()[1]:
        #    print("XD")

    # Clamp camera
    cam_pos[0] = max(0, min(cam_pos[0], map_size - max_cell_displayed))
    cam_pos[1] = max(0, min(cam_pos[1], map_size - max_cell_displayed))

    screen.fill((250, 250, 250))

    # Draw grid
    for i in range(max_cell_displayed + 1):
        offset = cell_size * i
        pygame.draw.line(screen, black, (offset, 0), (offset, max_cell_displayed * cell_size))
        pygame.draw.line(screen, black, (0, offset), (max_cell_displayed * cell_size, offset))

    # Draw map
    for x in range(max_cell_displayed):
        for y in range(max_cell_displayed):
            map_x = x + cam_pos[0]
            map_y = y + cam_pos[1]

            if 0 <= map_x < map_size and 0 <= map_y < map_size:
                value = map_data[map_y][map_x]

                if value == 1:
                    color = blue
                elif value == 2:
                    color = red
                elif value == 3:
                    color = green
                elif value == 4:
                    color = purple
                else:
                    color = black

                text = font.render(str(value), True, color)
                screen.blit(
                    text,
                    (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
                )
    
    # Draw minimap
    for x in range(map_size):
        for y in range(map_size):
            pygame.draw.rect(
                screen,
                (200, 200, 200) if map_data[y][x] == 0 else
                (0, 0, 255) if map_data[y][x] == 1 else
                (255, 0, 0) if map_data[y][x] == 2 else
                (0, 255, 0) if map_data[y][x] == 3 else
                (255, 255, 255),
                (
                    1056 + x * 2 - 63,
                    y * 2,
                    2,
                    2
                )
            )

    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (
            1056 + cam_pos[0] * 2 - 63,
            cam_pos[1] * 2,
            max_cell_displayed * 2,
            max_cell_displayed * 2
        ),
        2
    )

    # Draw menu
    pygame.draw.line(
        screen, (0, 0, 0),
        (1056 + 64, 0),
        (1056 + 64, window_height)
    )

    for x in range(3, window_height // 64):
        pygame.draw.line(
            screen, (0, 0, 0),
            (1056 - 128, x * 64),
            (window_width, x * 64)
        )    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
