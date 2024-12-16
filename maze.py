import pygame
import random

# Pygame setup
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

    def remove_walls(self, next_cell):
        dx = next_cell.x - self.x
        dy = next_cell.y - self.y
        if dx == 1:  # next_cell is to the right
            self.walls["right"] = False
            next_cell.walls["left"] = False
        elif dx == -1:  # next_cell is to the left
            self.walls["left"] = False
            next_cell.walls["right"] = False
        if dy == 1:  # next_cell is below
            self.walls["bottom"] = False
            next_cell.walls["top"] = False
        elif dy == -1:  # next_cell is above
            self.walls["top"] = False
            next_cell.walls["bottom"] = False


# Helper functions
def index(x, y):
    """Return the index of the cell at (x, y)."""
    if x < 0 or y < 0 or x >= cols or y >= rows:
        return None
    return x + y * cols


def get_neighbors(cell):
    """Return a list of unvisited neighbors for the given cell."""
    neighbors = []
    directions = [
        (0, -1),  # top
        (1, 0),  # right
        (0, 1),  # bottom
        (-1, 0),  # left
    ]
    for dx, dy in directions:
        neighbor_index = index(cell.x + dx, cell.y + dy)
        if neighbor_index is not None:
            neighbor = grid_cells[neighbor_index]
            neighbors.append(neighbor)
    return neighbors


def wilsons_algorithm():
    """Generate maze using Wilson's algorithm."""
    unvisited = grid_cells[:]
    visited = []

    # Randomly choose the first cell and mark it as visited
    current = random.choice(unvisited)
    current.visited = True
    visited.append(current)
    unvisited.remove(current)

    while unvisited:
        # Randomly pick a starting cell from the unvisited list
        start_cell = random.choice(unvisited)

        # Create a random walk path
        path = [start_cell]
        current = start_cell
        while current not in visited:
            neighbors = get_neighbors(current)
            next_cell = random.choice(neighbors)
            if next_cell in path:  # Loop detected, remove the loop
                loop_start = path.index(next_cell)
                path = path[: loop_start + 1]
            else:
                path.append(next_cell)
            current = next_cell

        # Carve out the path and mark cells as visited
        for i in range(len(path) - 1):
            path[i].remove_walls(path[i + 1])
            path[i].visited = True
            if path[i] in unvisited:
                unvisited.remove(path[i])
                visited.append(path[i])


# Create grid cells
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

# Generate maze using Wilson's algorithm
wilsons_algorithm()

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
