"""
Module for getting names of main colors on picture
"""

from __future__ import print_function, division
# image processing modules
from PIL import Image
import colorgram
import piexif
# color names
from lab_colors import colors_1500, colors_150, colors_20
# colormath modules
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

from string import upper, lower

from struct import unpack, pack
import os, sys


class NameTheColors(object):
    """
    Class for naming colors on the picture
    """
    thumb_size = 360, 360
    thumb_ext = '.thumbnail'

    def __init__(self, file):
        self.file = file
        self.colors_to_extract = 7
        self.outfile = os.path.splitext(self.file)[0] + self.thumb_ext
        if self._is_exists():
            self._create_thumb()
        else:
            raise NameError(
                "Could not find the file {}\{}".format(os.getcwd(), self.file))
        self.color_names = self._get_color_names()

    def _is_exists(self):
        return os.path.isfile(self.file)

    def _create_thumb(self):
        """Creates thumbnail"""
        if self.file != self.outfile:
            try:
                im = Image.open(self.file)
                im.thumbnail(self.thumb_size, Image.ANTIALIAS)
                im.save(self.outfile, "JPEG")
            except IOError:
                print("Cannot create thumbnail for {}".format(self.file))

    def _get_color_names(self, amount=3):
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
                      lab_color[1]) for lab_color in colorspace)
            min_delta = min(delta)
            return min_delta[1]

        def get_names(colors, colorspace):
            return set((name_the_color(color, colorspace) for color in colors))
        # main execution part

        # extract colorgram colors
        colors = colorgram.extract(self.outfile, self.colors_to_extract)
        # return only most interesting colors in order
        rgb_colors = get_rgb_coord(colors, 3)
        # convert them into LAB colorspace
        lab_colors = get_lab_coords(rgb_colors)
        # get colorspace objects for naming
        lab_1500 = get_colorspace(colors_1500)
        lab_150 = get_colorspace(colors_150)
        lab_20 = get_colorspace(colors_20)
        # union into final set all basic colors, 5 advanced colors and 2 super advanced colors
        all_color_names = get_names(lab_colors, lab_20)
        all_color_names.update(
            get_names(lab_colors[:5], lab_150),
            get_names(lab_colors[:2], lab_1500))

        return all_color_names

    def get_color_names(self):
        """
        Returns names of the colors of the picture
        """
        return self.color_names

    def _create_hashtags(self, h=False, case='', separator=';'):
        """
        h - boolean, set # symbol or not, default - True
        case - string U - upper, L - lower, default - initcap 
        """
        res = ''
        all_color_names = self.get_color_names()
        if h:
            preceding = '#'
        else:
            preceding = ''
        if case == 'U':
            mod_func = upper
        elif case == 'L':
            mod_func = lower
        else:
            mod_func = self._dummy
        l = len(separator)
        return res.join(preceding + mod_func(col) +
                       separator for col in all_color_names)[:-l]
        

    def _dummy(self, _):
        return _

    def _get_exif_keyword_tuple(self, in_str):
        """
        Returns in_str each symbol represented by int8u
        Currently only supports english 
        """
        #TODO: add correct unicode 
        tmp_str = in_str + chr(0)
        mask = str(len(tmp_str)) + "B" #insert B emoji here
        return tuple((item if not y else 0 for item in unpack(mask, tmp_str) for y in range(0, 2)))

    def _get_str_from_exif_keyword_tuple(self, in_tuple):
        """
        Returnc string encoded with previus function
        Currently only supports english 
        """
        filtered = tuple(filter(lambda x: x > 0, in_tuple))
        mask = str(len(filtered)) + 'B'
        return pack(mask, *filtered)

    def _set_hashtags(self):
        """
        Sets hashtags to a photos EXIF's keywords
        Replaces the keywords
        If exif doesn't exist - creates a dummy one
        """
        # dummy exif if its empty
        EXIF = {'Exif': {}, '0th': {34665: 2110, 40094: ()}, 'Interop': {}, '1st': {}, 'thumbnail': None, 'GPS': {}}
        im = Image.open(self.file)
        try:
            exif_dict = piexif.load(im.info["exif"])
        except KeyError:
            exif_dict = EXIF
        kw_tuple = self._get_exif_keyword_tuple(self._create_hashtags())
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = kw_tuple
        exif_bytes = piexif.dump(exif_dict)
        im.save(self.file, "jpeg", exif=exif_bytes)

    def _delete_thumb(self):
        """Deletes the tumbnail"""
        try:
            os.remove(self.outfile)
        except OSError:
            pass
