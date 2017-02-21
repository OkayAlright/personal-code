"""
level2Dgen.py
By Logan Davis

DESCRIPTION:
    A blender 2D platform level generator inspired by
    Spelunky's level system: http://tinysubversions.com/spelunkyGen2/
HOW-TO-USE:
    Import into blender and run as an external script.
    make sure that the instance of the object is using
    as absolute path to you source text to generate the
    level. Also make sure that the dimensions passed to
    ".run()" match the dimensions of your map.

HOW-TO-MAKE-A-MAP:
    The generator creates maps base off of plain text
    files. each character represents a block to be placed.
    Here is the legend of the block types:
        * 0 = wall
        * F = floor
        * D = door (entrance)
        * E = exit

2/14/17 | Python 3.6 / Blender 2.7 |
"""
import bpy

#tile_encodings = {
#   "0": "empty",
#   "F": "floor",
#   "D": "door",
#   "E": "exit"
#}


class terrain_translator(object):
    """ A spelunky-esque map generator """

    def __init__(self):
        self.map_as_string = None
        self.map_as_array = None

    def read_in_map(self, filename):
        """ loads a .txt "filename" in and reads it"""
        file = open(filename, "r")
        self.map_as_string = file.read()

    def generate_blank_map(self, dimensions):
        """
        Creates an empty map (no valid blocks codes).
        Width and height are read from "dimensions" in
        that order.
        """
        self.map_as_array = [[0 for z_index in range(0, dimensions[1])]
                             for x_index in range(0, dimensions[0])]

    def break_string_into_array(self, dimensions):
        """
        Parses the loaded map-string into a 2d array.
        Width and height are read from "dimensions" in
        that order.
        """
        self.map_as_array = list(filter((lambda x: x != []), (map(list, self.map_as_string.split("\n")))))
        if list(filter((lambda x: x == dimensions[1]), self.map_as_array )) == []:
            print("[WARNING]: passed height is not equal to height of source file.")
        elif list(filter((lambda x: x == dimensions[0]),self.map_as_array )) == []:
            print("[WARNING]: passed width is not equal to width of source file.")

        self.map_as_array.reverse()
        for row in self.map_as_array:
            row.reverse()

        print(self.map_as_array)

    def render_map(self):
        """
        Renders the loaded array-map in a blender scene.
        """
        for x_index in range(0, len(self.map_as_array)):
            for z_index in range(0, len(self.map_as_array[x_index])):
                if self.map_as_array[z_index][x_index] == "0":
                    x_coord = x_index * 2
                    y_coord = -2
                    z_coord = (z_index * 2) + 1
                elif self.map_as_array[z_index][x_index] == "F":
                    x_coord = x_index * 2
                    y_coord = 0
                    z_coord = (z_index * 2) + 1
                elif self.map_as_array[z_index][x_index] == "D":
                    continue
                elif self.map_as_array[z_index][x_index] == "E":
                    continue
                bpy.ops.mesh.primitive_cube_add(location=((x_coord, y_coord, z_coord)))

    def run(self, source_file, dimensions):
        """
        A wrapper to read in a map, parse it, and render it.

        ARGS:
        -------------------------
            * source_file: the txt that contains your map.
            * dimensions: the dimensions as a tuple (width, then height) of the map
        """
        self.read_in_map(source_file)
        self.break_string_into_array(dimensions)
        self.render_map()

t = terrain_translator()
t.run("/Users/ldavis/Documents/code/python/blenderUtils/test.txt",(7,7)) #replace path with your own abolute path

