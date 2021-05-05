import SpreadOfFire as simSeq
import SpreadOfFireJit as simPar
import time
import random

def average(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t

    avg = sum_num / len(num)
    return avg


if __name__ == '__main__':
    runMethodPerfCheck = False
    perfTestSeed = True
    runTimesEach = 1
    runSeq = True
    runPar = True

    iterations = 10
    gridSize = 2000
    probTree = 0.8
    probBurning = 0.01
    probImmune = 0.3
    probLighting = 0.001

    if runMethodPerfCheck:
        gridSize = 2000

    if perfTestSeed:
        seed = 675666552
    else:
        seed = random.randint(-2147483647, 2147483647)

    print("\n= Sim Stats =")
    print("Iterations:", iterations)
    print("Grid Size:", gridSize)
    print("Tree Probability:", probTree)
    print("Burning Probability:", probBurning)
    print("Immune Probability:", probImmune)
    print("Lightning Probability:", probLighting)
    print("Forest Seed:", seed)

    print("\n= Performance Stats =")

    if runMethodPerfCheck:
        seqRunTimesfg = []
        seqRunTimeseg = []
        seqRunTimessp = []
        parRunTimesfg = []
        parRunTimeseg = []
        parRunTimessp = []

        if runSeq:
            for i in range(runTimesEach):
                # No parallelisation
                startTime = time.time()
                fGridSeq = simSeq.forestGrid(probTree, probBurning, gridSize, seed)
                timeRan = (time.time() - startTime)
                seqRunTimesfg.append(timeRan)
                print("--- %s seconds - No Parallelisation (forestGrid) ---" % timeRan)

                startTime = time.time()
                exGridSeq = simSeq.extendGrid(fGridSeq)
                timeRan = (time.time() - startTime)
                seqRunTimeseg.append(timeRan)
                print("--- %s seconds - No Parallelisation (extendGrid) ---" % timeRan)

                startTime = time.time()
                simSeq.Spread(exGridSeq, probImmune, probLighting)
                timeRan = (time.time() - startTime)
                seqRunTimessp.append(timeRan)
                print("--- %s seconds - No Parallelisation (Spread) ---" % timeRan)

        if runPar:
            for i in range(runTimesEach):
                # parallelisation - Numba
                startTime = time.time()
                fGridPar = simPar.forestGrid(probTree, probBurning, gridSize, seed)
                timeRan = (time.time() - startTime)
                parRunTimesfg.append(timeRan)
                print("--- %s seconds - Parallelisation with Numba (forestGrid) ---" % timeRan)

                startTime = time.time()
                exGridPar = simPar.extendGrid(fGridPar)
                timeRan = (time.time() - startTime)
                parRunTimeseg.append(timeRan)
                print("--- %s seconds - Parallelisation with Numba (extendGrid) ---" % timeRan)

                startTime = time.time()
                simPar.Spread(exGridPar, probImmune, probLighting)
                timeRan = (time.time() - startTime)
                seqRunTimessp.append(timeRan)
                print("--- %s seconds - Parallelisation with Numba (Spread) ---" % timeRan)

        if runTimesEach > 1:
            print("\n= Averages =")
            if runSeq:
                print("--- %s seconds - No Parallelisation (forestGrid) [Avg.] ---" % average(seqRunTimesfg))
                print("--- %s seconds - No Parallelisation (extendGrid) [Avg.] ---" % average(seqRunTimeseg))
                print("--- %s seconds - No Parallelisation (Spread) [Avg.] ---" % average(seqRunTimessp))
            if runPar:
                print("--- %s seconds - Parallelisation with Numba (forestGrid) [Avg.] ---" % average(parRunTimesfg))
                print("--- %s seconds - Parallelisation with Numba (extendGrid) [Avg.] ---" % average(parRunTimeseg))
                print("--- %s seconds - Parallelisation with Numba (Spread) [Avg.] ---" % average(parRunTimessp))

    else:
        seqRunTimes = []
        parRunTimes = []

        if runSeq:
            for i in range(runTimesEach):
                # No parallelisation
                startTime = time.time()
                simSeq.Simulation(iterations, gridSize, seed, probTree, probBurning, probImmune, probLighting)
                timeRan = (time.time() - startTime)
                seqRunTimes.append(timeRan)
                print("--- %s seconds - No Parallelisation ---" % timeRan)

        if runPar:
            for i in range(runTimesEach):
                # parallelisation - Numba
                startTime = time.time()
                simPar.Simulation(iterations, gridSize, seed, probTree, probBurning, probImmune, probLighting)
                timeRan = (time.time() - startTime)
                parRunTimes.append(timeRan)
                print("--- %s seconds - Parallelisation with Numba ---" % timeRan)

        if runTimesEach > 1:
            print("\n= Averages =")
            if runSeq:
                print("--- %s seconds - No Parallelisation (Avg.) ---" % average(seqRunTimes))
            if runPar:
                print("--- %s seconds - Parallelisation with Numba (Avg.) ---" % average(parRunTimes))
