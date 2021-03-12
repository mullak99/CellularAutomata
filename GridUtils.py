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