import subprocess, time, random

def timeFunction(n,repeats,command):
    results = ""
    teststring = ""

    for i in range(n):
        teststring += str(random.randrange(0,10000)) + " "
        times = []
        print("Testing on string {}.",list(filter(None,teststring.split(" "))))
        for i in range(repeats):
            startTime = time.time()
            subprocess.run(command.split(" ")+list(filter(None, teststring.split(" "))))
            times.append(time.time() - startTime)
        average = sum(times)/repeats
        results += str(average) + "\n"
    
    f = open("results.txt","w")
    f.write(results)
    f.close()

timeFunction(100,5,"python subsetSum.py")
