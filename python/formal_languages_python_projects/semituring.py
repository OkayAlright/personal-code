class Turing_Machine(object):
    def __init__(self):
        self.running = True

        self.program = []
        self.reader_index = 0

        self.memory = [0]*100
        self.head_index = 0

        self.keywords = {">": self.moveRight, "<": self.moveLeft, "if": self.read, "write": self.write, "accept": self.accept_state, "reject": self.reject_state }

    def run(self):
        print(self.program[self.reader_index])
        try:
            self.keywords[self.program[self.reader_index]]()
            self.reader_index += 1
        except KeyError:
            print("Unrecognized operator: {}".format(self.program[self.reader_index]))
            quit()

    def accept_state(self):
        if self.memory[self.head_index] == self.program[self.reader_index + 1]:
            print("This machine exited in an accept state.")
            self.running = False
        self.reader_index += 1

    def reject_state(self):
        if self.memory[self.head_index] == self.program[self.reader_index + 1]:
            print("This machine exited in a reject state.")
            self.running = False
        self.reader_index += 1

    def write(self):
        self.memory[self.head_index] = self.program[self.reader_index +1]
        self.reader_index += 1

    def moveRight(self):
        if self.head_index == (len(self.memory) - 1):
            self.memory += [0] * 100
        self.head_index += 1

    def moveLeft(self):
        if self.head_index == 0:
            self.head_index += 100
            self.memory = ([0]*100) + self.memory
        self.head_index -= 1

    def read(self):
        read_value = self.memory[self.head_index]
        if read_value == (self.program[self.reader_index + 1]):
            self.reader_index += 2
            while(self.program[self.reader_index] != "else"):
                self.run()
            while(self.program[self.reader_index] != "then"):
                self.reader_index += 1
        else:
            while(self.program[self.reader_index] != "else"):
                self.reader_index += 1
            self.reader_index += 1
            while(self.program[self.reader_index] != "then"):
                self.run()

    def run_program(self):
        while self.running:
            self.run()
            if self.reader_index >= len(self.program):
                self.running = False

    def load_program(self,program_string):
        self.program = program_string.split()

t = Turing_Machine()
t.load_program("write 0 > > write 1 if 1 > 8 else < 7 accept 8 reject 7")
t.run_program()
print(t.reader_index)
print(t.program)
print(t.memory)
