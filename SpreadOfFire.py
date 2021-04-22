import numpy as np
import random
import cv2

def forestGrid(probTree, probBurning, size):  # Prob Tree = 0.8 , Prob Burning = 0.01
    grid = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            isBurn = random.random()
            isTree = random.random()
            if isTree < probTree:  # Been Switched from greater than
                if isBurn < probBurning:  # Been Switched from less than
                    grid[i, j] = 2
                else:
                    grid[i, j] = 1
            else:
                grid[i, j] = 0
    return grid


def extendGrid(grid):
    n = len(grid) + 2
    newGrid = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if (i == 0 or j == 0) or (i == n - 1 or j == n - 1):
                newGrid[i, j] = 3  # let 3 be the borders (later implement the reflected boundary)
            else:
                newGrid[i, j] = grid[i - 1, j - 1]
    return newGrid


def Spread(gridEx, probImmune, probLightning):
    n = len(gridEx) - 2
    newGrid = np.zeros((n, n))
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            isImmune = random.random()
            isLightning = random.random()
            # if Empty it will remain empty next time step
            if ((gridEx[i, j] == 2)):  # A burning cell becomes empty
                newGrid[i - 1, j - 1] = 0
            elif ((gridEx[i, j] == 1)):
                if (isLightning < probLightning or MooreNeighborHood(gridEx, i, j)):  # or grid[i-1][j-1] == 2
                    if (isImmune < probImmune):
                        newGrid[i - 1, j - 1] = 1
                    else:
                        newGrid[i - 1, j - 1] = 2
            else:  # An empty cell remains empty
                newGrid[i - 1, j - 1] = 0
    return newGrid


def MooreNeighborHood(grid, i, j):
    if grid[i - 1][j - 1] == 2 or grid[i + 1][j + 1] == 2 or grid[i + 1][j - 1] == 2 or grid[i - 1][j + 1] == 2 or \
            grid[i - 1][j] == 2 or grid[i][j + 1] == 2 or grid[i + 1][j] == 2 or grid[i][j - 1] == 2:
        isTrue = True
    else:
        isTrue = False
    return isTrue

def Simulation(time, forestGrid, probImmune=0.3, probLightning=0.001):
    grid = forestGrid
    gridList = [grid]

    for i in range(time):
        ext = extendGrid(grid)
        grid = Spread(ext, probImmune, probLightning)  # Immune - 0.3 , probLightning - 0.001
        gridList.append(grid)
        v_grid = visualise(grid)

        resized = cv2.resize(v_grid, (1000, 1000), interpolation=cv2.INTER_AREA)
        cv2.imshow("Forest Fire Spread", resized)
        cv2.waitKey(100)
    return gridList


def visualise(forestGrid):
    n = len(forestGrid)  # Maybe - 2?
    colorGrid = np.zeros((forestGrid.shape[0], forestGrid.shape[1], 3))

    for i in range(0, n):
        for j in range(0, n):
            if forestGrid[i, j] == 0:  # Empty Cell
                colorGrid[i, j, 0] = 1
                colorGrid[i, j, 1] = 1
                colorGrid[i, j, 2] = 1
            elif forestGrid[i, j] == 1:  # Blue - Tree
                colorGrid[i, j, 0] = 1
                colorGrid[i, j, 1] = 0
                colorGrid[i, j, 2] = 0
            elif forestGrid[i, j] == 2:  # Red - Burning Tree
                colorGrid[i, j, 0] = 0
                colorGrid[i, j, 1] = 0
                colorGrid[i, j, 2] = 1

    return colorGrid
