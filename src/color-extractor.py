import colorgram
from PIL import Image

colors = colorgram.extract(r'D:\python\auto-hashtag\src\input7.png', 6)

for color in colors:
    print(color.rgb)
    print(color.proportion)
    print("----")
