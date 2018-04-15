import colorgram
from PIL import Image

colors = colorgram.extract(r'D:\python\auto-hashtag\src\input7.png', 6)

for color in colors:
    print(color.hsl)
    print(color.proportion)
    print("----")

print("----_____------")

colors.sort(key=lambda x: x.hsl.s, reverse=True)


for color in colors:
    print(color.hsl)
    print(color.rgb)
    print(color.proportion)
    print("----")
