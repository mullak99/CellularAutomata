import SpreadOfFire as simSeq
import SpreadOfFireJit as simPar
import multiprocessing as mp
import cpuinfo
import time


if __name__ == '__main__':
    iterations = 5
    gridSize = 800
    probTree = 0.8
    probBurning = 0.01
    probImmune = 0.3
    probLighting = 0.001

    print("= CPU Stats =")
    print("CPU:", cpuinfo.get_cpu_info()["brand_raw"])
    print("CPU Arch:", cpuinfo.get_cpu_info()["arch_string_raw"])
    print("CPU threads:", mp.cpu_count())

    print("\n= Sim Stats =")
    print("Iterations:", iterations)
    print("Grid Size:", gridSize)
    print("Tree Probability:", probTree)
    print("Burning Probability:", probBurning)
    print("Immune Probability:", probImmune)
    print("Lightning Probability:", probLighting)

    # Row Normalisation of a 2D array
    fGrid = simSeq.forestGrid(probTree, probBurning, gridSize)

    print("\n= Performance Stats =")
    # No parallelisation
    startTime = time.time()
    simSeq.Simulation(iterations, fGrid, probImmune, probLighting)
    print("--- %s seconds - No Parallelisation---" % (time.time() - startTime))

    # parallelisation - Numba
    startTime = time.time()
    simPar.Simulation(iterations, fGrid, probImmune, probLighting)
    print("--- %s seconds - Parallelisation with Numba---" % (time.time() - startTime))