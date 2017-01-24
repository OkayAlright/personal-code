"""
generateLand.py
By Logan Davis

DESCRIPTION:
    This is a very simplistic procedural generator
    for hill, valleys, and mountains for Blender 2.7


    Currently is a slow toy, but hopefully after a
    few revisions it will be serviceable.

TO USE:
    Import this script into Blender as an external
    script. Edit the example value at the bottom
    of the file to suite your needs and then
    run the script.

TODOs:
    Improve literally everything about this.

1/23/17 | Python 3.5 / Blender 2.7 | LICENSE: MIT | MacOS 10.11
"""
import numpy as np
import random
import bpy


class LandGenerator (object):
    """
    A procedural generator for mountains and hills.

    Keyword Arguments:
    ----------------------------------------------
        * rule_spec: A dictionary containing 2 entries
                     (keys = "bottom" and "sides"). Both
                     entries should have a float between
                     0.0 and 1.0 as values.

                     These will be used as probabilities
                     for adjacent blocks to be spawned.

        * granularity: The size unit (in Blender location
                       units) that will be used when placing
                       blocks.

        * size: A set containing the X, Y, and Z  (in that order)
                dimensions of the block you want to generate.
    """
    def __init__(self, rule_spec=None, granularity=2, size=(100, 100, 100)):
        self.rule_spec = rule_spec
        self.map = None
        self.granularity = granularity
        self.dimensions = tuple(map((lambda x: x * self.granularity),
                                [size[1], size[0], size[2]]))  # change order xyz to yxz for indexing sanity

    def generate_base_3d_map(self):
        """ Generates a flat map of the dimensions specified upon instancing."""
        self.map = np.zeros(self.dimensions)
        for z in range(0, self.dimensions[1], self.granularity):
            for x in range(0, self.dimensions[2], self.granularity):
                self.map[0][z][x] = True

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

    def _calculate_spawn(self, y, z, x):
        """Helper function to determine whether a block should be spawned due to neighbors."""
        horizontal_transforms = [[0, 1, 0],
                                 [0, -1, 0],
                                 [0, 0, 1],
                                 [0, 0, -1]]
        if self.map[y-1, z, x] and (random.random() < self.rule_spec["bottom"]):
            return True
        for i in horizontal_transforms:
            if self.map[y+i[0], z+i[1], x+i[2]] and (random.random() < self.rule_spec["sides"]):
                return True

        return False

    def generate_3d_elevations(self):
        """Runs through the map using rule_spec to generate terrain."""
        for y in range(1, self.dimensions[0], self.granularity):
            for z in range(0, self.dimensions[1], self.granularity):
                for x in range(0, self.dimensions[2], self.granularity):
                    try:
                        if self.map[y, z, x]:
                            continue
                        self.map[y, z, x] = self._calculate_spawn(y, z, x)
                    except IndexError:
                        pass

    def run(self):
        """A wrapper to run the generator."""
        self.generate_base_3d_map()
        self.generate_3d_elevations()
        self.display_map()
        self.render_map_3d()

ruleProbs = {"bottom": 0.2, "sides": 0.6}

t = LandGenerator(ruleProbs, 1, (15, 15, 15))
t.run()


