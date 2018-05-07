"""
Module for getting names of main colors on picture
"""
from __future__ import print_function, division
import colorgram
from PIL import Image
from lab_colors import colors_1500, colors_150, colors_20
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import os
import sys


class NameTheColors(object):
    """
    Class for naming colors on the picture
    """
    thumb_size = 360, 360
    thumb_ext = '.thumbnail'

    def __init__(self, file):
        self.file = file
        self.colors_to_extract = 7
        try:
            self.outfile = os.path.splitext(self.file)[0] + self.thumb_ext
            # TODO find the actual exception
        except IOError:
            print("Incorrect file path")

    def _is_exists(self):
        return os.path.isfile(self.file)

    def _create_thumb(self, infile):
        if infile != self.outfile:
            try:
                im = Image.open(infile)
                im.thumbnail(self.thumb_size, Image.ANTIALIAS)
                im.save(self.outfile, "JPEG")
            except IOError:
                print("Cannot create thumbnail for {}".format(infile))

    def get_color_names(self, amount):
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

        def get_colorspace(scheme):
            """ Retruns list of mathcolor objects with names"""
            return [(LabColor(*color[0]), color[1]) for color in scheme]

        def name_the_color(color, colorspace):
            """ Tags the color with name
            color - colormath Labcolor
            return format - ((h, s, l), name)
            """
            delta = ((delta_e_cie2000(color, lab_color[0]),
                      color) for lab_color in colorspace)
            min_delta = min(delta)
            return min_delta[1]

        def get_names(colors, colorspace):
            return set((name_the_color(color, colorspace) for color in colors))
        # main execution part
        
        # extract colorgram colors
        colors = colorgram.extract(self.file, self.colors_to_extract)
        # return only most interesting colors in order
        rgb_colors = get_rgb_coord(colors, 3)
        # convert them into LAB colorspace
        lab_colors = get_lab_coords(rgb_colors)
        # get colorspace objects for naming
        lab_1500 = get_colorspace(colors_1500)
        lab_150 = get_colorspace(colors_150)
        lab_20 = get_colorspace(colors_20)
        all_color_names = set([])
        # union into final set all basic colors, 5 advanced colors and 2 super advanced colors
        all_color_names.union(get_names(lab_colors, lab_20))
        all_color_names.union(get_names(lab_colors[:5], lab_150))
        all_color_names.union(get_names(lab_colors[:2], lab_1500))
        return all_color_names

    def _create_hashtags(self):
        pass

    def _set_hashtags(self):
        pass
