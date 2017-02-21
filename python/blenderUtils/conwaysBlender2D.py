"""
conwaysBlender2D.py
By Logan Davis

DESCRIPTION:
    A simple 2d conways game of life script for
    use in blender.

    Generations are played on the X and Z axis,
    each generation is rendered progressively
    deeper on the Y axis.

TOUSE:
    Run as an internal script in Blender (tested on 2.7)

TODO:
    - Add wrapper logic for the board.
    - Allow caller to define what shapes to use when rendering.
    - Make a better interface to feed in start state.

CREDIT:
    - Jim Mahoney for the idea after explaining my failed
      3D conway attempt (too slow and buggy).

2/7/17 | Python 3.6 / Blender 2.7 | VScode 1.9

"""
import bpy

# INTERNAL NOTES ON WHAT'S WHAT:
# x = width, z = height, y = time
# 0 = Dead, 1 = Alive, 2 = going to die, 3 = going to live


class conwaysBlender2D(object):
    """
    A script to play Conway's Game of Life,
    skewing each generation on the Y axis.

    ARGS:
    ------------------------------------------
     * board_size: A tuple of the height and
                   width of the board.
     * generations: The number of generations
                    to play out.
    """
    def __init__(self, board_size=(10, 10), generations=10):
        self.width = board_size[0]
        self.height = board_size[1]
        self.board = [[0 for z_index in range(0, self.height)] for x_index in range(0, self.width)]
        self.max_generations = generations
        self.time_index = 0

    def display_board(self):
        """
        Echoes the current board state to STDOUT.
        """
        for x_index in range(0, self.width):
            print(self.board[x_index])

    def count_living_adj(self, x_coord, z_coord):
        """
        Counts the amount of living cells next to
        the passed in x and y co-ordinates.

        ARGS:
        -----------------------------------------
         * x_coord: the x co-ordinate of the cell
                    you wish to check.
         * y_coord: the y co-ordinate of the cell
                    you wish to check.
        """
        living_adj = 0
        for x_offset in range(-1, 2):
            for z_offset in range(-1, 2):
                if [x_offset, z_offset] != [0, 0]:
                    try:
                        if self.board[x_coord + x_offset][z_coord + z_offset] in [1, 2]:
                            living_adj += 1
                    except IndexError:
                        continue
                        #print("Logan, there was an indexing error. Fix this.")
        return living_adj

    def prep_board(self):
        """
        Sets up the board with markers
        of what cells live and what cells
        die.
        """
        for x_index in range(0, self.width):
            for z_index in range(0, self.height):
                numb_of_living_adj = self.count_living_adj(x_index, z_index)
                if self.board[x_index][z_index] == 1:
                    if numb_of_living_adj not in [2, 3]:
                        self.board[x_index][z_index] = 2
                else:
                    if numb_of_living_adj == 3:
                        self.board[x_index][z_index] = 3

    def step_generation(self):
        """
        Resolves prep markers (going to die or
        going to live). Ends with the board in
        a state where all cells are firmly dead
        or alive.
        """
        for x_index in range(0, self.width):
            for z_index in range(0, self.height):
                if self.board[x_index][z_index] == 2:
                    self.board[x_index][z_index] = 0
                elif self.board[x_index][z_index] == 3:
                    self.board[x_index][z_index] = 1

    def check_if_done(self):
        """
        Checks to see if the board
        is empty. If so, returns True
        """
        return sum([sum(column) for column in self.board]) == 0

    def run(self):
        """
        A wrapper and logic to
        run a coways game until
        self.max_generations is
        exceded or the board falls
        into a totally dead state.
        """
        while not self.check_if_done():
            self.display_board()
            self.prep_board()
            self.step_generation()
            self.render_in_3d()
            self.time_index += 1
            if self.time_index >= self.max_generations:
                break

    def render_in_3d(self):
        """
        renders the current board
        the a blender stage.
        """
        for x_index in range(0, self.width):
            for z_index in range(0, self.height):
                if self.board[x_index][z_index] == 1:
                    bpy.ops.mesh.primitive_cube_add(location=((x_index * 2),
                                                              (self.time_index * 3),
                                                              ((z_index * 2)+1)))

t = conwaysBlender2D((10, 10), 10) # instance object
#Set up a glider
t.board[3][3] = 1     
t.board[3][4] = 1
t.board[3][5] = 1
t.board[4][5] = 1
t.board[5][4] = 1
#run it.
t.run()
