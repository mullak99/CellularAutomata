import GridUtils as utils
import SpreadOfFire as sim

nGrid = sim.createForestGrid(0.75, 0.2, 10)
gridEx = sim.extendGridBoundary(nGrid)
gridSingleStep = sim.runSimulationOnce(nGrid, 0.2, 0.1)
gridMultiStep = sim.runSimulation(nGrid, 0.2, 0.1, 8)

utils.printGrid(nGrid, "Grid")  # Normal 10x10 Grid
utils.printGrid(gridEx, "GridEx")  # w/ boundary (12x12 with Normal 10x10 Grid inside)
utils.printGrid(gridSingleStep, "GridSingleStep")  # nGrid w/ a single timestep
utils.printGrids(gridMultiStep, "GridMultiStep")  # nGrid w/ a multi timesteps