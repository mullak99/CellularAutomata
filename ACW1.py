import GridUtils as utils
import SpreadOfFire as sim

nGrid = sim.createForestGrid(0.75, 0.2, 10)
gridMultiStep = sim.runSimulation(nGrid, 0.2, 0.1, 8)

utils.printGrids(gridMultiStep, "Simulation")