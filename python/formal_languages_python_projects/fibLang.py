"""
fibLang.py
Logan Davis

A parse and generator for the following language:

    - The Fibonacci numbers, in some suitable representation.

TO USE:
    import into some other script.
    If you wish to test whether a number is in
    the fibonacci sequence, use the parse() function.
    Otherwise, if you want to generate the sequence,
    us the generate() function.

12/10/16 | Python 3.5 | MacOS
"""

def parse(test_string):
    """
    Checks test_string to see
    if it is a fibonacci number.
    If yes, returns True.
    Else, returns False.
    """
    if test_string == "0":
        return True
    elif test_string =="1":
        return True
    try:
        x,y  = 1,1
        while int(test_string) > y:
             x,y = y,x+y
             if y == int(test_string):
                 return True
        return False # test_string is not a fib number
    except: 
        return False # test_string is not a number


def generate(n):
    """
    Returns the nth number
    if the fibonacci sequnce.
    """
    if n <= 1:
       y = 0
    elif (n == 2) or (n == 3):
       y = 1
    else:
        x,y = 1,1
        for i in range(n-3):
            x,y = y,x+y
    return y
