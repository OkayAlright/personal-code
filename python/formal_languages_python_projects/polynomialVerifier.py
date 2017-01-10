"""
polynomialVerifier.py


"""

def zeroSumVerifier(zeroSumCandidate):
    """
    returns True if list zeroSumCandidate
    sums to 0 and the list is not empty.

    else, returns False (sums to some 
    non-zero value).
    """
    sumOfList = 0
    if zeroSumCandidate == []:
        return False
    for i in zeroSumCandidate:
        sumOfList += i

    if sumOfList == 0:
        return True
    else:
        return False

import time


def timeFunction(n,repeats):
    results = ""
    testSolution = []

    for i in range(n):
        testSolution += [5,-5]
        times = []
        for i in range(repeats):
            startTime = time.time()
            zeroSumVerifier(testSolution)
            times.append(time.time() - startTime)
        average = sum(times)/repeats
        results += str(average) + "\n"
    
    f = open("resultsNPverifier.txt","w")
    f.write(results)
    f.close()

timeFunction(10000,5)
