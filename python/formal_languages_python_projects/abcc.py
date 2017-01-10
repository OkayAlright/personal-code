"""
abcc.py
Logan Davis

A parser and generator for the following language:
    - The set {(a^m)+(b^n)+(c^(m+n)) : m, n ≥ 0}.

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
    Verifies whether a test_string is part of the abcc_lang spec.
    If yes, returns True. Else, returns False.
    """
    stage = 1
    test_string = list(test_string)

    if test_string == []:
        return True

    while stage == 1:
        if (test_string == []):
            break        

        try:
            front = test_string.pop(0)
            end = test_string.pop()
        except IndexError:
            return False

        if (front  == "a") and (end == "c"):
            continue
        elif (front == "b") and (end  == "c"):
            stage = 2
        else:
            return False
    while stage == 2:
        if (test_string == []):
            break

        try: 
            front = test_string.pop(0)
            end = test_string.pop()
        except IndexError:
            return False

        if (front == "b") and (end == "c"):
            continue
        else:
            return False
    return True

def generate(n, verbose=False):
    """
    Returns an unorder list of strings in abcc_lang up to n
    where n is the length of m+n (the "c" half of the strings
    length).

    set verbose to True to see all strings as they are generated.
    """
    collection = []
    queue = []
    while True:
        if queue != []:
            current_working_string = queue.pop(0)
            a = "a"+current_working_string+"c"
            b_sections = current_working_string.split("c",1)
            b_sections[1] += "c"
            b = b_sections[0] + "bc" + b_sections[1]
        else:
            a = "ac"
            b = "bc"

        if verbose:
            print(a)
            print(b)
        queue.append(a) ; collection.append(a)
        queue.append(b) ; collection.append(b)
        if len(queue[0])//2 == n:
            return list(set(collection))
