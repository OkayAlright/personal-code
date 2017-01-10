"""
geneticTS.py

By Logan Davis | 10/25/15

   Description: A genetic solution to the Traveling Saleman
                problem for the AI Midterm.

Python 2.7 | Editor: Emacs | Distro: Ubuntu 15
"""
import random, math

class Citizen(object):
    """
    Citizen is small object meant to be used by 
    an instance of a TravelingSalesmen object.
    All the Citizen class can do is hold two 
    attributes: route (it's planned travelsal
    through a series of locations) and fitness
    (the distance of that route. The smaller,
     the better).
    """
    def __init__(self,route = None, fitness = 0):
        self.route = route
        self.fitness = fitness
    
class TravelingSalesmen(object):
    """
    OVERVIEW:
        A genetic algorithm class to generate answers to the 
    Traveling Salesmen problem. 

    HOW TO USE:
        This simplist way to use this is by creating an instance
    of this class, and then call self.generate() where self is the 
    instance you just created. However this method can be slow 
    because you have to enter each location in one at a time. 
    One of the optional arguements is to directly assign an
    organized route to the route arguement. An organized is a list
    of locations, each location is a list containing a name/identifier
    as the first element, an x co-ord as the second, and a y co-ord
    as the last. EXAMPLE OF LOCATION:
                      ["Jutland", 45, 2000.3]
    After either directly assigning these locations in a list, you still have
    call the self.generate() method, but it will skip constructing a route and
    just generate an answer. If you don't directly assign a route, after you 
    input the route through a prompt, it will generate the answer with no
    further method calls.

    A self.generate call returns an instance of a Citizen object. That returned
    instance will contain the best route and its fitness.
    
    OPTIONAL ARGS:
          - generations = the amount of gerneations the algorithm will run.
          - populationSize = the amount of different possible answers (Citizens)
                             the algorithm will use in generating an answer.
          - retention = the amount of the population that is kept at the culling
                        phase based on their fitness.
          - mutationRate = the chance of mutations occuring within self.population
          - route = the collection of locations you wish to traverse
    
    NOTE:
       To test this class, a test route has been provided. 
    It is creatively named testRoute.

    ---------------------------DOCTTEST-------------------------------
    >>> ts = TravelingSalesmen(10,10,0.2,0.01,testRoute)
    >>> answer = ts.generate()
    >>> print math.floor(answer.fitness) #floor to deal with float rounding
    9003.0
    >>>
    """
    
    def __init__(self,generations = 1000,populationSize = 1000,retention = 0.2,mutationRate = 0.01,route = []):
        """
        All stored values for any instance of this class.
        """
        self.population = []                     #The entire population of Citizen instances
        self.route = route                       #The collection of all locatons
        self.generations = generations           #The number of generations/iterations to find an answer
        self.retention = retention               #The size of the population that lives on each generation
        self.populationSize = populationSize     #The Total allowed size of self.population
        self.mutationRate = mutationRate         #The chance of a mutation occuring in self.population
        self.bestCitizen = None                  #The best citizen found, meaning the lowwest (shortest) fitness score.
        
    def __str__(self):
        """
        This makes it so that any printing of an instance 
        of this object will give the best route through the 
        locations in self.route and the fitness score of that 
        route.
        """
        return "Best route: {} with a fitness of {}.".format(self.bestCitizen.route,self.bestCitizen.fitness)

    def generate(self):
        """
        generate actually runs the algorithm.
        If the instance this is invoked upon
        already has a route, it just runs, 
        otherwise is calls constructRoute
        to create a list of locations first.
        The results are stored in self.bestCitizen.
        Then the instance held in self.bestCtitizen 
        are returned.
        ----------------DOCTEST-----------------
        >>> ts = TravelingSalesmen(100,100,0.2,0.01,testRoute)
        >>> answer = ts.generate()
        >>> ts._fitness(answer)
        >>> math.floor(answer.fitness)  #to deal with rounding of precision
        9003.0
        >>> 
        """
        if self.route == []:
            self.constructRoute()
        self._createPopulation()
        for i in xrange(0,self.generations):
            self._repopulate()
        self._organizePopulation()
        self.bestCitizen = self.population[0]
        return self.bestCitizen

    def constructRoute(self):
        """
        constructRoute prompts the user to enter a 
        series of locations and their x & y co-ordinates.
        These locations are stored as a list in
        self.route. The function exits if the user
        inputs any of the strings held in 
        possibleStops after entering a location.
        """
        done = False
        possibleStops = ["y","yes","YES","Yes","STOP","stop","Stop","Fuck off"]
        while done != True:
            location = []
            location.extend([raw_input("What is the location's name?"),\
                             input("What is the x co-ordinate?"),\
                             input("What is the y co-ordinate?")])
            self.route.append(location)
            answer = raw_input("Are you done? (y/n)")
            if answer in possibleStops:
                done = True
            
    def _createPopulation(self):
        """
        _createPopulation generates citizens
        each with a randomized list of the 
        elements of self.route. The number of 
        these citizens are defined by self.populationSize
        and they are all appended to self.population
        """
        copyRoute = self.route[:] #makes shallow copy, random.shuffle operates in-place
        for i in xrange(0,self.populationSize):
            self.population.append(Citizen())
        for citizen in self.population:
            citizen.route = self.route[:]
            random.shuffle(citizen.route)

    def _repopulate(self):
        """
        _repopulate is a wrapper to call
        _organizePopulation, _cullAndRefill,
        and _mutate in order.
        """
        self._organizePopulation()
        self._cullAndRefill()
        self._mutate()

    def _organizePopulation(self):
        """
        _organizePopulation evalutes the fitness of each citizen 
        and then sort them from most fit (lowwest distance) to 
        least fit (largest distance).
        -----------------------DOCTEST---------------------------
        >>> ts = TravelingSalesmen(1,2,0.2,0.01,testRoute)
        >>> ts._createPopulation()
        >>> ts._organizePopulation()
        >>> (ts.population[0].fitness < ts.population[1].fitness) \
            or (ts.population[0].fitness == ts.population[1].fitness)
        True
        >>>
        """
        for citizen in self.population:
            self._fitness(citizen)
        self._rankPopulation()

    def _cullAndRefill(self):
        """
        _cullAndRefill takes to top % of self.population (% defined in self.retention)
        then repopulates the pool of citizens in self.populate based on the routes of 
        the fit population (those retained after culling).

        Crossover method: take two random citizens, if their first and second halves
                          don't match, take the frist half from and and add it to the
                          first half of the other. Give that to a new citizen in the
                          population. If the halves do have some over lap, grab another 
                          random citizen and test the first citizena and this new one until
                          a non-redundant match is found or the limit of tries is reached.
                          if the limit is reached, just make a copy of the first random citizen.
        ------------------------------------DOCTEST------------------------------------------
        >>> ts = TravelingSalesmen(2,10,0.2,0.01,testRoute)
        >>> ts._createPopulation()
        >>> ts._organizePopulation()
        >>> comparison = ts.population
        >>> ts._cullAndRefill()
        >>> (len(ts.population) == len(comparison)) \
             and (ts.population != comparison)
        True
        >>>
        """
        middle = len(self.route)/2
        fitPopulation = self.population[:int(math.floor(len(self.population)*self.retention))]
        newPopulation = fitPopulation[:]
        for i in xrange(len(self.population)-len(fitPopulation)):
            citizen1 = fitPopulation[random.randint(0,len(fitPopulation)-1)]
            for i in xrange(0,(10*len(fitPopulation))):
                citizen2 = fitPopulation[random.randint(0,len(fitPopulation)-1)]
                if self.matchFinder(citizen1,citizen2,middle) == True:
                    newPopulation.append(Citizen())
                    newPopulation[-1].route = citizen1.route[:middle] + citizen2.route[middle:]
                    self.population = newPopulation[:]
                    break
                elif(i == (10*len(fitPopulation))-1):
                    newPopulation.append(Citizen())
                    newPopulation[-1].route = citizen1.route
        self.population = newPopulation[:]

    def _mutate(self):
        """
        _mutate iterates through the entire
        self.population. If a random.random()
        call returns a value <= self.mutationRate,
        then two random locations in a single 
        citizen's route are flipped.
        """
        for i in xrange(0,len(self.population)):
            if random.random() <= self.mutationRate:
                index1 = random.randint(0,len(self.route)-1)
                index2 = random.randint(0,len(self.route)-1)
                copy = self.population[i] .route[index1]
                self.population[i].route[index1] = self.population[i].route[index2]
                self.population[i].route[index2] = copy
        
            
    def _fitness(self, citizen):
        """
        _fitness evaluates the fitness of
        citizen. The measure of this 
        fitness is the distance of that 
        citizen's route. distance is 
        calculated using the standard 
        xy distance formula.

        Take 1 arguement:
           citizen = some citizen instance
        ---------------DOCTEST-----------------
        >>> citizen = Citizen(testRoute)
        >>> ts = TravelingSalesmen()
        >>> ts.route = citizen.route
        >>> ts._fitness(citizen)
        >>> math.floor(citizen.fitness) #floored to deal with rounding
        10208.0
        >>>
        """
        distance = 0
        for i in xrange(0,len(self.route)):
            if i < (len(self.route) - 1):
                xDistance = abs(citizen.route[i][1] - citizen.route[i+1][1])
                yDistance = abs(citizen.route[i][2] - citizen.route[i+1][2])
            else:
                xDistance = abs(citizen.route[i][1] - citizen.route[0][1])
                yDistance = abs(citizen.route[i][2] - citizen.route[0][2])
            distance += math.sqrt((xDistance**2)+(yDistance**2))
        citizen.fitness = distance

    def _rankPopulation(self):
        """
        sorts self.population, in place, by each citizens fitness.
        """
        self.population = sorted(self.population, key=lambda citizen: citizen.fitness)

    def matchFinder(self,citizen1,citizen2,cut):
        """
        matchFinder takes two citizen instances,
        compares slices of thier routes and
        returns true if there is no over lap
        and false if there is any redundance.
        
        Takes 3 arguements:
            citizen1 = some citizen instance 
            citizen2 = some other citizen instance
            cut = where you are slicing their routes
        
        -----------------DOCTEST--------------------
        >>> ts = TravelingSalesmen()
        >>> citizen1 = Citizen([["jutland",45,2000],\
                              ["flemington",456,2],\
                              ["clinton",3456,234],\
                              ["highland",300,20]])
        >>> citizen2 = Citizen([["clinton",3456,234],\
                                ["highland",300,20],\
                                ["jutland",45,2000],\
                                ["flemington",456,2]])
        >>> ts.matchFinder(citizen1,citizen2,2)  #overlapping route halves
        False
        >>> citizen1.route = citizen1.route[:2]  #non-overlapping
        >>> citizen2.route = citizen2.route[:2]
        >>> ts.matchFinder(citizen1,citizen2,1)
        True
        """
        firstHalf = citizen1.route[:cut]
        secondHalf = citizen2.route[cut:]
        for i in firstHalf:
            for x in secondHalf:
                if x == i:
                    return False
        return True

#The Test Route provided
testRoute = [["jutland",45,2000],["flemington",456,2],["clinton",3456,234],["highland",300,20]]

if __name__ == "__main__":
    import doctest
    doctest.testmod()