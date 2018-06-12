"""
Module for getting names of main colors on picture
"""

from __future__ import print_function, division
# image processing modules
from PIL import Image
import colorgram as cg
# color names
from lab_colors import colors_1500, colors_150, colors_20
# colormath modules
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

import os
import sys


class NameTheColors(object):
    """
    Class for naming colors on the picture
    colors_to_extract - int, number of color for extraction
    """

    def __init__(self, colors_to_extract=7):
        self.colors_to_extract = colors_to_extract
        self.lab_1500 = self._get_colorspace(colors_1500)
        self.lab_150 = self._get_colorspace(colors_150)
        self.lab_20 = self._get_colorspace(colors_20)

    def _get_colorspace(self, scheme):
        """ Retruns list of mathcolor objects with names"""
        return [(LabColor(*color[0]), color[1]) for color in scheme]

    def _get_color_names(self, im, amount=3):
        """Returns names of the colors"""

        def get_rgb_coord(colors, amount):
            """colors - list of colorgram colors
               amount - amount of top colors
               returns ordered list of colorgram colors"""
            by_area = colors[:]
            by_area.sort(key=lambda x: x.proportion, reverse=True)
            by_area = by_area[:amount]
            by_sat = colors[:]
            by_sat.sort(key=lambda x: x.hsl.s, reverse=True)
            by_sat = by_sat[:amount]
            ordered_col = []
            for i in range(amount):
                ordered_col.append(by_area[i])
                ordered_col.append(by_sat[i])
            return ordered_col

        def get_lab_coords(colors):
            """colors - set of colorgram colors
               returns list of colormath LAB colors"""
            return [convert_color(sRGBColor(*color.rgb, is_upscaled=True), LabColor)
                    for color in colors]

        def name_the_color(color, colorspace):
            """ Tags the color with name
            color - colormath Labcolor
            return format - ((h, s, l), name)
            """
            delta = ((delta_e_cie2000(color, lab_color[0]),
                      lab_color[1]) for lab_color in colorspace)
            min_delta = min(delta)
            return min_delta[1]

        def get_names(colors, colorspace):
            return set((name_the_color(color, colorspace) for color in colors))
        # main execution part
        # extract colorgram colors
        colors = cg.extract(im.tmb, self.colors_to_extract)
        # return only most interesting colors in order
        rgb_colors = get_rgb_coord(colors, 3)
        # convert them into LAB colorspace
        lab_colors = get_lab_coords(rgb_colors)
        # union into final set all basic colors, 5 advanced colors and 2 super advanced colors
        all_color_names = get_names(lab_colors, self.lab_20)
        all_color_names.update(
            get_names(lab_colors[:5], self.lab_150),
            get_names(lab_colors[:2], self.lab_1500))

        return all_color_names
