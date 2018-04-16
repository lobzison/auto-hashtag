import colorsys
from colors150 import colors_150


def hex_to_rgb_to_hsl(hex):
    hlen = len(hex)
    rgb = tuple(int(hex[i:i + hlen / 3], 16)
                for i in range(0, hlen, hlen / 3))
    hls = colorsys.rgb_to_hls(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
    return [round(hls[0] * 360, 3), round(hls[2] * 100, 3), round(hls[1] * 100, 3)]


colors = [[line[0], line[1].title()] for line in colors_150]

print(colors)

#new_colors = [[hex_to_rgb_to_hsl(line[0]), line[1]] for line in colors]

for line in colors:
    print(str(line)+',')
