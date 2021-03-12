import GridUtils as utils
import SpreadOfFire as sim

simulationGrids = sim.runSimulation(0.75, 0.2, 0.2, 0.1, 10, 8)

utils.printGrids(simulationGrids, "Fire Spread Simulation")  # Simulation Grids