"""
dfa.py
by Logan Davis

A simple (simple in making, not using) collection of functions
& a class to simulate DFA's

11/14/16 | Python 3.5 | Editor: Nano
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

def start_computing(node,input_string):
    """
    A wrapper for compute() that allows 
    the input you want to test to be 
    typed as a string.
    """
    compute(node,list(input_string))

#States in the DFA
q1 = node()
q2 = node()
q3 = node()
q4 = node()
#Transition Table between states
q1.branches = {"0":q1,"1":q2}
q2.branches = {"1":q2,"0":q3}
q3.branches = {"1":q4,"0":q3}
q4.branches = {"0":q4,"1":q4}
#Define Accept states in the DFA
q1.accept_state = True
q3.accept_state = True
#Call start_computing and pass in
#the starting node and a test input
start_computing(q1,"111000")

