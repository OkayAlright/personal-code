#!/usr/bin/env python3
"""
turingYaml.py
By Logan Davis

DESCRIPTION:
    A programmable turing machine
    that consumes a turing specification
    in turning machine language yvtm
    (yaml virtual turing machine).

TO-HOW-USE:
    $ ./turingYaml.py <yvtm file>

    OPTIONAL FLAGS:
     "--verbose": Print intermediate states of
                  the machine during run time.

DEPENDENCIES:
     PyYAML(http://pyyaml.org)

10/10/16 | Python 3.5 | MIT License
"""
import yaml, argparse

class TuringMachine(object):
    def __init__(self):
        self.halt = False            #Should we halt?
        self.accept_states = None    #What states do we accept?
        self.accept = False          #Should we accept?
        self.reject_states = None    #What states do we reject?
        self.reject = False          #Should we reject?

        self.state = None            #Current state
        self.spec = None             #The yvtm as dict
        self.tape = None             #working tape
        self.reader_index = 0        #current position on the tape

        self.debug = False           #verbose mode?

        self.parse_args()            #set up the machine.

    def parse_args(self):
        """
        Handles command line args
        and loads the yvtm file
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("yvtm_file",help="The *.yvtm spec for the turing machine.")
        parser.add_argument("--verbose",help="Print out each step of the machine as it runs.",action="store_true")
        args =  parser.parse_args()
        self.load_spec(args.yvtm_file)
        if args.verbose:
            self.debug = True

    def check_state(self):
        """
        Checks to see if self.state is 
        in either  self.accept_states or 
        self.reject_states and flips
        self.accept or self.reject if either
        is true.
        """
        if self.state in self.accept_states:
            self.accept = True
        elif self.state in self.reject_states:
            self.reject = True

    def _set_mem(self, memory_state):
        """
        Sets self.tape to arg memory state
        and resets the tape reader to the 
        left most position.
        """
        self.tape = memory_state
        self.reader_index = 0

    def print_state(self):
        """
        Prints out every step of the machines
        program. Only invoked when the
        '--verbose' flag is used
        """
        state = ""
        for i in range(0,len(self.tape)):
            if i == self.reader_index:
                state += " <" + self.tape[i] + ">"
            else:
                state += " "+self.tape[i]
        state += " : " + self.state
        print(state)

    def run(self):
        """
        Runs the yvtm until it enters
        an accept, reject, or halt state.
        """
        while((not self.accept) and (not self.reject) and (not self.halt)):
            if self.debug:
                self.print_state()
            self.resolve_step()
            self.check_state()
        if self.accept:
            print("GOOD: Machine ended in Accept state")
        elif self.reject:
            print("BAD: Machine ended in Reject state")
        elif self.halt:
            print("HALT: No transition rule.")
        else:
            print("ERROR: The machine has entered a strange state.")

    def move_tape(self,direction):
        """
        Moves reader head to the left
        or right depending of arg 'direction'
        and will extend the tape if need be.
        """
        if direction == 'left':
            if self.reader_index ==  0:
                self.extend_tape('left')
            self.reader_index -= 1
        elif direction == 'right':
            if self.reader_index == (len(self.tape) - 1):
                self.extend_tape('right')
            self.reader_index += 1
        else:
            print("ERROR: Directtion {} is not valid")
            quit()

    def resolve_step(self):
        """
        Resolves a single step of the
        yvtm and tells the machine to
        halt if no transition is specificied.
        """
        for transition in self.spec['machine']:
            trigger = list(map((lambda x : str(x)), transition[:2]))
            if [self.state,self.tape[self.reader_index]] == trigger:
                self.state = transition[2]
                self.tape[self.reader_index] = str(transition[3])
                self.move_tape(transition[4])
                return #return if a transition triggered
        self.halt = True

    def load_spec(self, yamlfile):
        """
        Loads arg yamlfile (a yvtm file)
        into a dictionary and applies its
        spec to the running machine.
        """
        self.spec = yaml.load(open(yamlfile,"r"))
        self.state = self.spec['start']
        self.accept_states = self.spec['accept']
        self.reject_states = self.spec['reject']
        self.tape = list(self.spec['tape'])

    def extend_tape(self, side):
        """
        Extends the tape to arg 'side'
        by one slot and moves to head
        accordingly.
        """
        if side in ["r","right","R"]:
            self.tape =  self.tape + [self.spec['blank']]
        elif side in ["l","L","left"]:
            self.tape = [self.spec['blank']] + self.tape
            self.reader_index += 1
        else:
            print("ERROR: direct {} is not valid".format(side))
            quit()

t = TuringMachine() # instance it
t.run()             # and run it
