"""
blender3Drender.py
By Logan Davis


1/23/17 | Python 3.5 / Blender 2.7 | LICENSE: MIT | MacOS 10.11
"""
import numpy as np
import bpy


class baseRenderScript (object):
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
    def __init__(self, granularity=2, size=(100, 100, 100)):
        self.map = None
        self.granularity = granularity
        self.dimensions = tuple(map((lambda x: x * self.granularity),
                                [size[1], size[0], size[2]]))  

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
                    if self.map[y, z, x]:
                        bpy.ops.mesh.primitive_cube_add(location=(x-(self.dimensions[2]/2),
                                                                  z-(self.dimensions[1]/2),
                                                                  y+1))

    def delete_all_on_layer(self):
        """ Deletes all objects on the default layer."""
        bpy.ops.object.select_by_layer()
        bpy.ops.object.delete(use_global=False)





