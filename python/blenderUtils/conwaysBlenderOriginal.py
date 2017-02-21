"""
conwaysBlender.py
By Logan Davis


1/23/17 | Python 3.5 / Blender 2.7 | LICENSE: MIT | MacOS 10.11
"""
import numpy as np
import bpy


class conwaysBlender(object):
    """
    A basic class for 3d rendering scripts to use.

    Keyword Arguments:
    ----------------------------------------------

        * granularity: The size unit (in Blender location
                       units) that will be used when placing
                       blocks.

        * size: A set containing the X, Y, and Z  (in that order)
                dimensions of the block you want to generate.
    """
    def __init__(self, size=(100, 100, 100)):
        self.map = None
        self.granularity = 1
        self.dimensions = tuple(map((lambda x: x * self.granularity),
                                [size[1], size[0], size[2]]))  
        self.generate_empty_3d_map()

    def generate_empty_3d_map(self):
        """ Generates an empty map of the dimensions specified upon instancing."""
        self.map = np.zeros(self.dimensions)

    def display_map(self):
        """ Prints the map to the console for debugging purposes."""
        print(self.map)

    def render_map_3d(self):
        """Places cubes in Blender scene based on self.map"""
        for y in range(0, self.dimensions[0], self.granularity):
            for z in range(0, self.dimensions[1], self.granularity):
                for x in range(0, self.dimensions[2], self.granularity):
                    if self.map[y, z, x] == 1:
                        bpy.ops.mesh.primitive_cube_add(location=(x-(self.dimensions[2]/2),
                                                                  z-(self.dimensions[1]/2),
                                                                  y+1))

    def check_if_done(self):
        """ yup """
        return sum(sum(sum(self.map)))

    def run(self):
        while True:
            self.step_generation()
            self.finalize_step()
            self.display_map()
            self.render_map_3d()
            if self.check_if_done():
                break
            self.delete_all_on_layer()


    def delete_all_on_layer(self):
        """ Deletes all objects on the default layer."""
        bpy.ops.object.select_by_layer()
        bpy.ops.object.delete(use_global=False)

    def step_generation(self):
        """yup"""
        for y in range(0, self.dimensions[0], self.granularity):
            for z in range(0, self.dimensions[1], self.granularity):
                for x in range(0, self.dimensions[2], self.granularity):
                    self.map[y, z, x] = self.judge_liveliness(x, y, z)

    def finalize_step(self):
        """yup"""
        for y in range(0, self.dimensions[0], self.granularity):
            for z in range(0, self.dimensions[1], self.granularity):
                for x in range(0, self.dimensions[2], self.granularity):
                    if self.map[y, z, x] == 2:
                        self.map[y, z, x] = 1
                    elif self.map[y, z, x] == 3:
                        self.map[y, z, x] = 0

    def judge_liveliness(self, x, y, z):
        """
        0 = Dead
        1 = Alive
        2 = coming to life
        3 = going to die
        """
        cell_state = self.map[y, z, x]
        living_adj = 0

        for y_off in range(-1, 2):
            for z_off in range(-1, 2):
                for x_off in range(-1, 2):
                    if ([x_off, y_off, z_off] != [0, 0, 0]) and\
                     (self.map[y_off, z_off, x_off] in [1, 3]):
                        living_adj += 1
        if cell_state == 1:
            if (living_adj < 8) or (living_adj > 1): #should stay alive
                return 1
            else:         #should die
                return 3
        elif cell_state == 0:
            if living_adj == 5:
                return 2      #should come alive
            else:
                return 0      #should stay dead


t = conwaysBlender((10,10,10))
t.map[5,5,5] = 1
t.map[5,6,5] = 1
t.map[5,4,5] = 1
t.run()






