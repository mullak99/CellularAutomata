import random
from copy import copy, deepcopy
import numpy as np
import cv2


def createForestGrid(probTree, probBurning, n):
    grid = [[0 for x in range(n)] for y in range(n)]  # Create grid with size n x n

    for i in range(n):
        for j in range(n):
            isTree = random.random()
            if (isTree < probTree):  # Coord is a tree (since isTree is less than random float [0.0-1.0])
                isBurn = random.random()
                if (isBurn < probBurning):
                    grid[i][j] = 2  # Tree is burning (since isBurning is less than random float [0.0-1.0])
                else:
                    grid[i][j] = 1  # Tree is NOT burning (since isBurning is greater than random float [0.0-1.0])
            else:
                grid[i][j] = 0  # Coord is a tree (since isTree is greater than random float [0.0-1.0])
    return grid


def extendGridBoundary(grid):
    n = len(grid) + 2  # Length of 'grid' plus two (1x boundry around original grid)
    newGrid = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            if ((i == 0 or j == 0) or (i == n - 1 or j == n - 1)):
                newGrid[i][j] = "B"  # If is first column OR first row OR last column OR last row
            else:
                newGrid[i][j] = grid[i - 1][j - 1]  # If is any other row
    return newGrid

def removeGridBoundary(grid):
    n = len(grid) - 2  # Length of 'grid' minus two (1x boundry around original grid)
    newGrid = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        if (i > 0 and i < n):
            for j in range(n):
                if(j > 0 and j < n):
                    newGrid[i - 1][j - 1] = grid[i][j]
    return newGrid

def runSimulationOnce(grid, probImmune, probLightning):
    gridE = extendGridBoundary(grid)
    n = len(gridE)
    pGrid = [[0 for x in range(n)] for y in range(n)]
    n = len(pGrid)
    for i in range(n):
        for j in range(n):
            nIm = i - 1
            nIp = i + 1
            nJm = j - 1
            nJp = j + 1
            isImmune = random.random()
            if (gridE[i][j] == 1 and (isImmune < probImmune)):
                isLightning = random.random()
                if (((nIm > 0 and gridE[nIm][j] == 2) or (nIp < n and gridE[nIp][j] == 2) or (
                        nJm > 0 and gridE[i][nJm] == 2) or (nJp < n and gridE[i][nJp] == 2))):
                    if (isImmune < probImmune and gridE[i][j] == 1):
                        pGrid[i][j] = 2  # A neighbour is burning AND this tree isn't immune
                    else:
                        pGrid[i][j] = gridE[i][j]
                elif (isLightning < probLightning):
                    pGrid[i][j] = 2  # Tree was struck by lightning
            elif (gridE[i][j] == 2):
                pGrid[i][j] = 0
            else:
                pGrid[i][j] = gridE[i][j]
    rGrid = removeGridBoundary(pGrid)
    return rGrid


def runSimulation(grid, probImmune, probLightning, times):
    grids = [None] * times
    for i in range(times):
        if (i > 0):
            gridNext = grids[i - 1]
        else:
            gridNext = grid
        grids[i] = runSimulationOnce(gridNext, probImmune, probLightning)
    return grids


def printGrid(grid, name="None"):
    print("Grid:", name)
    lines = []
    for row in grid:
        lines.append(' '.join(str(x) for x in row))
    print('\n'.join(lines), "\n")


def printGrids(grids, name="None"):
    print("Grids:", name)
    for i in range(len(grids)):
        printGrid(grids[i], (name, i))


nGrid = createForestGrid(0.75, 0.2, 10)
gridEx = extendGridBoundary(nGrid)
gridSingleStep = runSimulationOnce(nGrid, 0.2, 0.1)
gridSingleStepRemove = removeGridBoundary(gridSingleStep)
gridMultiStep = runSimulation(nGrid, 0.2, 0.1, 8)

printGrid(nGrid, "Grid")  # Normal 10x10 Grid
printGrid(gridEx, "GridEx")  # w/ boundary (12x12 with Normal 10x10 Grid inside)
printGrid(gridSingleStep, "GridSingleStep")  # nGrid w/ a single timestep
printGrid(gridSingleStepRemove, "GridSingleStepRemove")  # gridSingleStep w/ boundary removed
printGrids(gridMultiStep, "GridMultiStep")  # nGrid w/ a multi timesteps
