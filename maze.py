import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Define constants
WIDTH, HEIGHT = 1280, 720
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE  # Number of columns and rows in the grid


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def draw(self, screen):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(screen, pygame.Color("black"), (x, y, TILE, TILE))

        if self.walls["top"]:
            pygame.draw.line(
                screen, pygame.Color("darkorange"), (x, y), (x + TILE, y), 2
            )
        if self.walls["right"]:
            pygame.draw.line(
                screen, pygame.Color("darkorange"), (x + TILE, y), (x + TILE, y + TILE), 2
            )
        if self.walls["bottom"]:
            pygame.draw.line(
                screen, pygame.Color("darkorange"), (x + TILE, y + TILE), (x, y + TILE), 2
            )
        if self.walls["left"]:
            pygame.draw.line(
                screen, pygame.Color("darkorange"), (x, y + TILE), (x, y), 2
            )


# Create grid cells
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
current_cell.visited = True
stack = []

# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen
    screen.fill("purple")

    # Draw cells
    for cell in grid_cells:
        cell.draw(screen)

    # Flip display
    pygame.display.flip()

    # Limit FPS
    clock.tick(60)

pygame.quit()
