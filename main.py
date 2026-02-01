import pygame

# Constants
run = True
map_size = 64
map_data = []
window_width = 1024 + 128 + 128
window_height = 960 + 32
cell_size = 32
max_cell_displayed = 32 - 1

# Camera starts in center
cam_pos = [map_size // 4 + 1,  map_size // 4 + 1]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("T1")
font = pygame.font.SysFont(None, 16)
clock = pygame.time.Clock()

# Functions
def map_gen(size):
    result = []
    center = size // 2
    for y in range(size):
        row = []
        for x in range(size):
            value = max(abs(x - center), abs(y - center))
            row.append(value)
        result.append(row)
    return result

# Initialize map
map_data = map_gen(map_size)
print(map_data)
# Main loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                cam_pos[1] -= 1
            if event.key == pygame.K_s:
                cam_pos[1] += 1
            if event.key == pygame.K_a:
                cam_pos[0] -= 1
            if event.key == pygame.K_d:
                cam_pos[0] += 1

    # Clamp camera 
    cam_pos[0] = max(0, min(cam_pos[0], map_size - max_cell_displayed))
    cam_pos[1] = max(0, min(cam_pos[1], map_size - max_cell_displayed))

    screen.fill((250, 250, 250))

    # Draw grid
    for i in range(max_cell_displayed + 1):
        offset = cell_size * i
        pygame.draw.line(
            screen, (0, 0, 0),
            (offset, 0),
            (offset, max_cell_displayed * cell_size - 1)
        )
        pygame.draw.line(
            screen, (0, 0, 0),
            (0, offset),
            (max_cell_displayed * cell_size - 1, offset)
        )


    # Draw values safely
    for x in range(max_cell_displayed):
        for y in range(max_cell_displayed):
            map_x = x + cam_pos[0]
            map_y = y + cam_pos[1]

            if 0 <= map_x < map_size and 0 <= map_y < map_size:
                value = map_data[map_y][map_x]
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(
                    center=(x * cell_size + cell_size // 2,
                            y * cell_size + cell_size // 2)
                )
                screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
