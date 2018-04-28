import colorgram
from PIL import Image
from lab_colors import colors_1500, colors_150, colors_20
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import os
import sys

name = 6
size = 360, 360
infile = r'{}.jpg'.format(name)

outfile = os.path.splitext(infile)[0] + ".thumbnail"
if infile != outfile:
    try:
        im = Image.open(infile)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(outfile, "JPEG")
    except IOError:
        print "cannot create thumbnail for '%s'" % infile

colors = colorgram.extract(r'{}.thumbnail'.format(name), 12)


def get_colors_names(colors, colorspace):
    return [name_the_color(color, colorspace) for color in colors]


def name_the_color(color, colorspace):
    """ Tags the color with name
    color - tuple with (h, s, l)
    return format - ((h, s, l), name)
    """
    dist = ((delta_e_cie2000(color, lab_color[0]),
             color, lab_color[1], lab_color[0]) for lab_color in colorspace)
    min_dist = min(dist)
    return min_dist


def get_colorspace(scheme):
    """ Retruns list of mathcolor objects with names"""
    return [(LabColor(*color[0]), color[1]) for color in scheme]

def convert_rgb_to_lab(color):
    """ Converts colorgram's HSL to colormath's Lab """
    return convert_color(sRGBColor(*color.rgb, is_upscaled=True), LabColor)


by_area = colors[:]
by_area.sort(key=lambda x: x.proportion, reverse=True)
by_area = [convert_rgb_to_lab(color) for color in by_area]

by_sat = colors[:]
by_sat.sort(key=lambda x: x.hsl.s, reverse=True)
by_sat = [convert_rgb_to_lab(color) for color in by_sat]


lab_1500 = get_colorspace(colors_1500)
lab_150 = get_colorspace(colors_150)
lab_20 = get_colorspace(colors_20)

print("area colors:")
area_names = get_colors_names(by_area, lab_1500)
area_names = [c[2] for c in area_names]
print(set(area_names[:2]))
area_names = get_colors_names(by_area, lab_150)
area_names = [c[2] for c in area_names]
print(set(area_names[:3]))
area_names = get_colors_names(by_area, lab_20)
area_names = [c[2] for c in area_names]
print(set(area_names[:5]))

print("saturation colors:")
sat_names = get_colors_names(by_sat, lab_1500)
sat_names = [c[2] for c in sat_names]
print(set(sat_names[:2]))
sat_names = get_colors_names(by_sat, lab_150)
sat_names = [c[2] for c in sat_names]
print(set(sat_names[:3]))
sat_names = get_colors_names(by_sat, lab_20)
sat_names = [c[2] for c in sat_names]
print(set(sat_names[:5]))
