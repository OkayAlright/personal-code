import sys

def _subsetSum(setRemaining, subset):
    if (sum(subset) == 0) and (subset != []):
        #print("0-Sum FOUND: {}.".format(subset))
        quit()
    elif (setRemaining != []):
        for i in reversed(range(len(setRemaining))):
            newSetRemaining = setRemaining[:i+1]
            newSubset = subset[:]; newSubset.append(newSetRemaining.pop(i))
            _subsetSum(newSetRemaining,newSubset)

def findSubsetSum(setToTest):
    _subsetSum(setToTest,[])
    #print("No 0-sum subsets were found.")

setToTest = []

for i in range(1,len(sys.argv)):
    setToTest.append(int(sys.argv[i]))
findSubsetSum(setToTest)
