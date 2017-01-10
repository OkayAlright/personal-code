"""
zero_and_one.py
by Logan Davis

A simple dfa to recognize the following language:

    - The subset of {0, 1}∗ whose strings have even length 
      and no more than 3 contiguous 1’s.

TO USE: import into some other script and call 
        start_computing(<the sring you want to test>)

        The result will be printed to stdout 

12/10/16 | Python 3.5 | MacOS
"""
class node(object):
    """
    A simple class to act as a node in a DFA.
    branches is a dict that the key would be the
    character to handle and it's value would be
    the corresponding transition.

    accept_state signifies that that is an 
    acceptable state to end in.
    """
    def __init__(self,branches={},accept=False):
        self.branches = branches
        self.accept_state = accept

def compute(node,input):
    """
    Controls the flow of an input given a node
    to start and the input (as list) to be computed
    """
    if input == []:
        if node.accept_state:
            print("Input is a valid string")
        else:
            print("Input is non-valid, ended in non-accept state")
    else:
        if input[0] in node.branches:
            compute(node.branches[input.pop(0)],input)
        else:
            print("Input is nonvalid, unhandled input was encountered: {}".format(input[0]))

#states
start = node()
even0 = node()
odd0 = node()
o1 = node()
o2 = node()
o3 = node()
e1 = node()
e2 = node()
e3 = node()
death = node()
#transition table
start.branches = {"0":odd0,  "1":e1    }
even0.branches = {"0":odd0,  "1":e1    }
odd0.branches =  {"0":even0, "1":o1    }
e1.branches =    {"0":even0, "1":e2    }
e2.branches =    {"0":odd0,  "1":e3    }
e3.branches =    {"0":even0, "1":death }
o1.branches =    {"0":odd0,  "1":o2    }
o2.branches =    {"0":even0, "1":o3    }
o3.branches =    {"0":odd0,  "1":death }
death.branches = {"0":death, "1":death }
#accept states
even0.accept_state = True
o1.accept_state = True
o3.accept_state = True
e2.accept_state = True
# run

def start_computing(input_string,node=start):
    """
    A wrapper for compute() that allows 
    the input you want to test to be 
    typed as a string.
    """
    compute(node,list(input_string))
