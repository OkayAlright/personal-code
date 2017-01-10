"""
mine sweeper clone
 yup
"""
import random

welcome = """
Welcome to:

 _____                             _                   _   
|_   _|   ___   _ __   _ __ ___   (_)  _ __     __ _  | |  
  | |    / _ \ | '__| | '_ ` _ \  | | | '_ \   / _` | | |  
  | |   |  __/ | |    | | | | | | | | | | | | | (_| | | |  
  |_|    \___| |_|    |_| |_| |_| |_| |_| |_|  \__,_| |_|  
                                                            
  ____                                                  
 / ___|  __      __   ___    ___   _ __    _   _   _ __ 
 \___ \  \ \ /\ / /  / _ \  / _ \ | '_ \  | | | | | '__|
  ___) |  \ V  V /  |  __/ |  __/ | |_) | | |_| | | |   
 |____/    \_/\_/    \___|  \___| | .__/   \__, | |_|   
                                  |_|      |___/        

V1.0 | Written using Python 3.5
"""
#Large text from http://www.messletters.com/en/big-text/

class minesweeper(object):
    def __init__(self):
        self.x_size = 0
        self.y_size = 0
        self.board = []
        self.mask = []

        self.difficulty = 0

        print(welcome,end="\n\n")

    def init_size(self):
        need_dimensions = True
        while need_dimensions:
            user_input = input("What size board so you want (first width then height): ")
            co_ords = user_input.split(" ")
            try:
                self.x_size = int(co_ords[0])
                self.y_size = int(co_ords[1])
                if (self.x_size > 99) or (self.x_size < 2) or (self.y_size > 99) or (self.y_size < 2):
                    print("ERROR: Be reasonable. Please input x and y values between 2 and 99")
                    continue
                need_dimensions = False
            except:
                print("ERROR: please enter two numbers such as '5 5'")

    def set_difficulty(self):
        need_answer = True
        while need_answer:
            print("Please choose a difficulty:\n\n\t1 = Easy\n\n\t2 = Medium\n\n\t3 = Hard\n")
            user_input = input("Please type 1, 2, or 3: ")
            try:
                self.difficulty = int(user_input)
                need_answer = False
            except:
                print("ERROR: Please type 1, 2, or 3.")

    def place_bombs(self):
        for y in range(self.y_size):
            for x in range(self.x_size):
                if (random.randint(0,10) < self.difficulty):
                    self.board[y][x] = "B"

    def place_markers(self):
        for y in range(self.y_size):
            for x in range(self.x_size):
                self.set_number(x,y)

    def set_number(self,x,y):
        adj_bombs = 0
        transforms = [(0,1),(0,-1),(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1)]
        for tup in transforms:
                try:
                    if ((x == 0) and (tup[0] == -1)) or ((y == 0) and (tup[1] == -1)):
                        continue
                    if self.board[y+tup[1]][x+tup[0]] == "B":
                        adj_bombs += 1
                except IndexError:
                    continue
        if adj_bombs != 0 and self.board[y][x] != "B":
            self.board[y][x] = str(adj_bombs)

    def gen_board_structure(self):
        for y in range(self.y_size):
            self.board.append([" "]*self.x_size)
            self.mask.append(["H"]*self.x_size)

    def print_board(self):
        x_nums = ""
        for x in range(1,self.x_size+1):
            if x < 10:
                x_nums += " "+str(x)+" "
            else:
                x_nums += " "+str(x)

        print("\n    "+x_nums+"\n    " + "---"*self.x_size)
        for y in range(self.y_size):
            print("{:>2d} |".format(y+1),end="")
            for x in range(self.x_size):
                if self.mask[y][x] == "H":
                    print(" ~ ", end="")
                elif self.mask[y][x] == "M":
                    print(" M ", end="")
                else:
                    print(" {} ".format(self.board[y][x]), end="") 
            print("|")
        print("    " + "---"*self.x_size)

    def reveal_board(self):
        print(" " + "^^^"*self.x_size)
        for y in range(self.y_size):
            print("<",end="")
            for x in range(self.x_size):
                print(" {} ".format(self.board[y][x]), end="")
            print(">")
        print(" " + "vvv"*self.x_size)

    def get_player_move(self):
        need_move = True
        while need_move:
            print("Please enter 'm' to 'mark' or 'c' to 'uncover' followed by")
            user_input = input("x and y co-ordinates: ")
            co_ords = user_input.split(" ")
            try:
                if (co_ords[0].upper() != "C") and (co_ords[0].upper() != "M"):
                    print("ERROR: unrecognized command. Please enter 'c' for uncover or 'm' for mark.")
                    continue
                x = int(co_ords[1]) - 1
                y = int(co_ords[2]) - 1
                if ((x < 0) or (x > self.x_size - 1)) or ((y < 0) or (y > self.y_size - 1)):
                    print("ERROR: enter a valid x and y value (what you entered is off the board)")
                    continue
                need_move = False
            except:
                print("ERROR: please enter two numbers such as '5 5'")
        return (co_ords[0].upper(),x,y)

    def uncover(self):
        self.print_board()
        move = self.get_player_move()
        if move[0] == "C":
            self.demask(move[1],move[2])
            self.check_bomb(move[1],move[2])
        elif move[0] == "M":
            self.mark(move[1],move[2])

    def mark(self,x,y):
        self.mask[y][x] = "M"

    def check_bomb(self,x,y):
        if self.board[y][x] == "B": #OH NO
            self.explode()

    def explode(self):
        self.reveal_board()
        print("BOOM! Game Over...")
        self.display_score()
        quit()

    def display_score(self,count_bombs=False):
        score = 0
        for y in range(self.y_size):
            for x in range(self.x_size):
                if self.mask[y][x] == " ":
                    score += 100
                if (self.board[y][x] == "B") and count_bombs:
                    score += 1000
        score *= self.difficulty
        print(("-"*60)+"\nFINAL SCORE: {}\n".format(score))

    def verifyVictory(self):
        for y in range(self.y_size):
            for x in range(self.x_size):
                if (self.board[y][x] != "B") and \
                   ((self.mask[y][x] == "H") or \
                   (self.mask[y][x] == "M")):
                    return False
        return True

    def win(self):
        self.print_board()
        print("~~~!!! WINNER !!!~~~")
        self.display_score(count_bombs=True)
        quit()

    def demask(self,x,y):
        self.mask[y][x] = " "
        if self.board[y][x] == " ":
            transforms = [(0,1),(0,-1),(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1)]
            for tup in transforms:
                try:
                    if ((x == 0) and (tup[0] == -1)) or ((y == 0) and (tup[1] == -1)):
                        continue
                    if self.mask[y+tup[1]][x+tup[0]] == "H":
                        self.demask(x+tup[0],y+tup[1])
                except IndexError:
                    continue # hit edge of board

    def set_up(self):
        self.init_size()
        self.set_difficulty()
        self.gen_board_structure()
        self.place_bombs()
        self.place_markers()

    def run(self):
        self.set_up()
        while True:
            self.uncover()
            if self.verifyVictory():
                self.win()

game = minesweeper()
game.run()
