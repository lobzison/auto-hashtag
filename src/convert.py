from __future__ import division
import colorsys
from colormath.color_objects import HSLColor, LabColor
from colormath.color_conversions import convert_color
from colors20 import colors_20


def hex_to_rgb_to_hls(hex):
    hlen = len(hex)
    rgb = tuple(int(hex[i:i + hlen / 3], 16)
                for i in range(0, hlen, hlen / 3))
    hls = colorsys.rgb_to_hls(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
    return [round(hls[0] * 360, 3), round(hls[2] * 100, 3), round(hls[1] * 100, 3)]


new_colors = [[list(convert_color(HSLColor(
    col[0][0] / 360, col[0][1] / 100, col[0][2] / 100), LabColor).get_value_tuple()), col[1]] for col in colors_20]

new_colors = [
    [
        [round(val, 2) for val in color[0]], color[1]
    ]
    for color in new_colors]

for line in new_colors:
    print(str(line)+',')