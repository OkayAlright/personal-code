"""
paren_bracket.py
Logan Davis

A parser and generator for the following language:
    - The language with symbols (, ), [ and ] whose 
      valid strings are those with correctly 
      matching and nested parentheses and brackets.

TO USE:
    import into some other script.
    If you wish to test whether a number is in
    the fibonacci sequence, use the parse() function.
    Otherwise, if you want to generate the sequence,
    us the generate() function.

12/10/16 | Python 3.5 | MacOS
"""

def parser(test_string):
    """
    Will test is a string is in the language paren_brac language
    if yes, returns True. Else returns False.
    """
    if (test_string == ""):
        return True
    elif ((test_string[0] == "[") and (test_string[-1] == "]")) or\
         ((test_string[0] == "(") and (test_string[-1] == ")")):
        return parser(test_string[1:-1])
    else:
        return False

def generate(n, verbose=False):
    """
    Returns an unordered list of strings in paren_brac lang
    out to n where n is the number of paired symbols in the 
    string.

    Set Verbose to True if you want to see every string
    as they are being generated.
    """
    collection = []
    queue = [""]
    while True:
        current_inner_string = queue.pop(0)
        paren = "(" + current_inner_string + ")"
        brac = "[" + current_inner_string + "]"
        if verbose:
            print(paren)
            print(brac)
        queue.append(paren) ; collection.append(paren)
        queue.append(brac) ; collection.append(brac)
        if len(queue[0])//2 == n:
            return list(set(collection))
