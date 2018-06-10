import colorgram
from PIL import Image
from colors1500 import colors_1500
from colors150 import colors_150
from colors20 import colors_20
from math import sqrt
import os, sys
import colorsys

name = 4
size = 360, 360
infile = r'./{}.jpg'.format(name)

outfile = os.path.splitext(infile)[0] + ".thumbnail"
if infile != outfile:
    try:
        im = Image.open(infile)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(outfile, "JPEG")
    except IOError:
        print "cannot create thumbnail for '%s'" % infile

colors = colorgram.extract(r'./{}.thumbnail'.format(name), 12)


print("----_____------")

by_area = [color for color in colors]
by_area.sort(key=lambda x: x.proportion, reverse=True)

by_sat = [color for color in colors]
by_sat.sort(key=lambda x: x.hsl.s, reverse=True)


# colors.sort(key=lambda x: x.hsl.s, reverse=True)


# for color in colors:
#     print(color.hsl)
#     print(color.rgb)
#     print(color.proportion)
#     print("----")

def get_colors_names(colors, scheme):
    return [name_the_color(color, scheme) for color in colors]

def name_the_color(color, scheme):
    """ Tags the color with name
    color - tuple with (h, s, l)
    return format - ((h, s, l), name)
    """
    gen = ((find_closest(color, hsl_color[0]), color, hsl_color) for hsl_color in scheme)
    res = min(gen)
    return res



def find_closest(color, hsl2):
    """
       returns double with distance
    """
    if isinstance(color, tuple):
        return sqrt((color[0] - hsl2[0]) ** 2 + (color[1]- hsl2[1]) ** 2 + (color[2] - hsl2[2]) ** 2)
    else:
        return sqrt((color.hsl.h-hsl2[0]) ** 2 + (color.hsl.s-hsl2[1]) ** 2 + (color.hsl.l-hsl2[2]) ** 2)


# print("area colors:")
# area_names = get_colors_names(by_area, colors_1500)
# area_names = [c[1] for c in area_names]
# print(set(area_names[:1]))
# area_names = get_colors_names(by_area, colors_150)
# area_names = [c[1] for c in area_names]
# print(set(area_names[:2]))
# area_names = get_colors_names(by_area, colors_20)
# area_names = [c[1] for c in area_names]
# print(set(area_names[:3]))

# print("saturation colors:")
# sat_names = get_colors_names(by_sat,colors_1500)
# sat_names = [c[1] for c in sat_names]
# print(set(sat_names[:1]))
# sat_names = get_colors_names(by_sat,colors_150)
# sat_names = [c[1] for c in sat_names]
# print(set(sat_names[:2]))
# sat_names = get_colors_names(by_sat,colors_20)
# sat_names = [c[1] for c in sat_names]
# print(set(sat_names[:3]))

print (colors[0].hsl.h, colors[0].hsl.s, colors[0].hsl.l)

true_hsl = colorsys.rgb_to_hls(colors[0].rgb.r / 255.0, colors[0].rgb.g / 255.0, colors[0].rgb.b / 255.0)
true_hsl = (true_hsl[0] * 360, true_hsl[2] * 100, true_hsl[1] * 100)
print(true_hsl)

print('-----')

print (name_the_color(true_hsl, colors_1500))

