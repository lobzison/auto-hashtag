"""
Module for getting names of main colors on picture
"""
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

    def __init__(self, name, folder=None):
        self.folder = folder
        self.name = name
        if folder is None:
            self.path = name
        else:
            self.path = folder + name
        self.colors_to_extract = 7

    def _is_exists(self):
        return os.path.isfile(self.path)

    def _create_thumb(self):
        outfile = os.path.splitext(self.path)[0] + thumb_ext
        if infile != outfile:
            try:
                im = Image.open(infile)
                im.thumbnail(thumb_size, Image.ANTIALIAS)
                im.save(outfile, "JPEG")
            except IOError:
                print "Cannot create thumbnail for '%s'" % infile

    def get_color_names(self):
        colors = colorgram.extract(, self.colors_to_extract)

    def _create_hashtags(self):
        pass

    def _set_hashtags(self):
        pass

    def _get_color_name(self):
        pass

    def _get_colorspace(self):
        pass

    def _convert_rgb_to_lab(self):
        pass
