"""
PCPfinder.py
By Logan Davis

QUESTION (sipser 2nd ed. - pg 211):
    Find a match for the following instance of the Post
    Correspondence Problem.
    
    {[ab/abab],[b/a],[aba/b],[aa/a]}

DESCRIPTION:
    I trusted Sipser that there was a match to this question,
    so I wrote a queue-based solution finder for the problem.

    A queue is used to store each possible n-length combination
    of dominos. The queue helps avoid non-terminating loops (as
    opposed to a stack) by switching between branches of the 
    computation every iteration. 

    It turns out sipser was not lying to me by telling be to
    find a match. :)  

    Some example output (truncated):
    $python PCPfinder.py
    python3 PCPfinder.py 
    iter 1...
    CHECKING: [('ab', 'abab')].
    iter 2...
    CHECKING: [('b', 'a')].
    iter 3...
    CHECKING: [('aba', 'b')].

    (some many iterations)...

    iter 327...
    CHECKING: [('aa', 'a'), ('aa', 'a'), ('ab', 'abab'), ('aba', 'b')].
    iter 328...
    CHECKING: [('aa', 'a'), ('aa', 'a'), ('ab', 'abab'), ('aa', 'a')].
    iter 329...
    CHECKING: [('aa', 'a'), ('aa', 'a'), ('b', 'a'), ('ab', 'abab')].
    FOUND: [('aa', 'a'), ('aa', 'a'), ('b', 'a'), ('ab', 'abab')].

    The timing is quite reasonable:
    $time python PCPfinder.py
        real    0m0.051s
        user    0m0.035s
        sys     0m0.010s

TO-USE:
    Edit the list of dominos to a list of tuple that represent 
    the dominos you are working with (that are known to have a
    solution). Run the program. Cross your fingers.


Python 3.5 | 11/2/16 | License MIT
"""

dominos = [("ab","abab"),("b","a"),("aba","b"),("aa","a")] 
queue = [] # a queue for lists of pair to be tested

def check_match(possible_match):
    """
    Takes a list of two-tuples (each index containing
        a string).
    Returns true if the concat of all tuples first 
        indexes matches the concat of the second.
    Otherwise returns false.
    """
    top = ""
    bottom = ""
    for tup in possible_match:
        top += tup[0]
        bottom += tup[1]
    return top == bottom

def _setup():
    """
    Preloads the collection of dominos into the 
    queue in the desired format.
    """
    for item in dominos:
        queue.append([item])

def find_match():
    """
    Steps through the queue, testing each sub-list
    for a match. If no match is found, take the current item,
    and stack a copy in the queue for each type on domino (appended
    to the copy). If a match is found, stops and prints the correct
    sequence.
    """
    _setup()
    itera = 0
    not_matched = True
    while not_matched:
        itera += 1
        print("iter {}...".format(itera))
        item = queue.pop(0)
        print("CHECKING: {}.".format(item))
        if check_match(item):
            print("FOUND: {}.".format(item))
            break
        else:
            for i in dominos:
                queue.append(item + [i])

find_match()
        
