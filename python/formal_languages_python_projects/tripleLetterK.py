input_string = [0,0,0,1,1,1,2,2,2]
tape = range(0,101)

def main(input_tape, output_tape):
    index = 0
    startedTwos = False
    
    while(input_tape[index] == 1):
        if index == 0:
            input_tape = ["x"] + input_tape
        index += 1
        
    while(input_tape[index] == 2):
        if startedTwos == False:
            input
