import numpy as np
import random
import cv2

# Creates a new grid representing a forest, some trees start on-fire (probBurning)
def forestGrid(probTree, probBurning, size, seed):
    random.seed(seed)  # Allows forest generation to be the same, useful for performance checks
    grid = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            isTree = random.random()
            if isTree < probTree:  # isTree & probTree are 0.0-1.0. This cell will be a tree
                isBurn = random.random()
                if isBurn < probBurning:  # isBurn & probBurning are 0.0-1.0
                    grid[x, y] = 2  # This cell is a burning tree
                else:
                    grid[x, y] = 1  # This cell is a normal tree
            else:
                grid[x, y] = 0
    return grid

# Extends the current grid, adding a boundary (3) around all current cells
def extendGrid(grid):
    n = len(grid) + 2
    newGrid = np.zeros((n, n))  # New grid, extends boundary (+2)
    for x in range(n):
        for y in range(n):
            if (x == 0 or y == 0) or (x == n - 1 or y == n - 1):
                newGrid[x, y] = 3  # Boundary cells are represented by a 3
            else:
                newGrid[x, y] = grid[x - 1, y - 1]
    return newGrid

# Calculates fire spread of entire grid for one iteration
def Spread(gridEx, probImmune, probLightning):
    n = len(gridEx) - 2
    newGrid = np.zeros((n, n))  # New grid, removes boundary (-2)
    for x in range(1, n + 1):
        for y in range(1, n + 1):
            if gridEx[x, y] == 1:  # Current cell is a tree
                isLightning = random.random()  # RNG for lightning strike
                if isLightning < probLightning or MooreNeighbourhood(gridEx, x, y):
                    isImmune = random.random()  # RNG for immunity
                    if isImmune < probImmune:
                        newGrid[x - 1, y - 1] = 1  # Tree is immune
                    else:
                        newGrid[x - 1, y - 1] = 2  # Tree is near another on-fire tree, or was hit by lightning
                else:
                    newGrid[x - 1, y - 1] = 1
            else:  # Burning cells and other empty cells become/remain empty
                newGrid[x - 1, y - 1] = 0
    return newGrid


# Checks if any of the eight cells (inc. diagonal) around the current cell are on fire, if so, return true
def MooreNeighbourhood(grid, x, y):
    if grid[x - 1][y - 1] == 2 or grid[x + 1][y + 1] == 2 or grid[x + 1][y - 1] == 2 or grid[x - 1][y + 1] == 2 or \
            grid[x - 1][y] == 2 or grid[x][y + 1] == 2 or grid[x + 1][y] == 2 or grid[x][y - 1] == 2:
        return True
    return False

# Checks if any of the four cells (not inc. diagonal) around the current cell are on fire, if so, return true
def VonNeumanNeighbourhood(grid, x, y):
    if grid[x - 1][y - 1] == 2 or grid[x + 1][y + 1] == 2 or grid[x + 1][y - 1] == 2 or grid[x - 1][y + 1] == 2:
        return True
    return False

# Runs the entire simulation for a preset time (no. of iterations)
def Simulation(time, size, forestSeed, probTree=0.8, probBurning=0.01, probImmune=0.3, probLightning=0.001):
    grid = forestGrid(probTree, probBurning, size, forestSeed)  # Creates the grid for the forest
    gridList = [grid]  # Adds initial grid to a list/array

    for _ in range(time):  # Run simulation for preset number of iterations
        ext = extendGrid(grid)  # Extend grid (add boundary)
        grid = Spread(ext, probImmune, probLightning)  # Apply fire spread rules to the grid
        gridList.append(grid)  # Adds grid to a list/array
        v_grid = visualise(grid)  # Calculates the colours for the current grid

        resized = cv2.resize(v_grid, (1000, 1000), interpolation=cv2.INTER_AREA)  # Visualise the current grid
        cv2.imshow("Spread of Forest Fire", resized)
        cv2.waitKey(100)
    return gridList


# Creates a visual representation of the forest grid, colouring the appropriate cells
def visualise(forestGrid):
    n = len(forestGrid)
    colorGrid = np.zeros((forestGrid.shape[0], forestGrid.shape[1], 3))
    for x in range(0, n):
        for y in range(0, n):
            if forestGrid[x, y] == 0:  # 0 = Empty Cell
                colorGrid[x, y, 0] = 1
                colorGrid[x, y, 1] = 1
                colorGrid[x, y, 2] = 1
            elif forestGrid[x, y] == 1:  # 1 = Normal Tree (Green)
                colorGrid[x, y, 0] = 0
                colorGrid[x, y, 1] = 1
                colorGrid[x, y, 2] = 0
            elif forestGrid[x, y] == 2:  # 2 = Burning Tree (Red)
                colorGrid[x, y, 0] = 0
                colorGrid[x, y, 1] = 0
                colorGrid[x, y, 2] = 1
    return colorGrid
