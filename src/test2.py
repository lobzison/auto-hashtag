import matplotlib.pyplot as plt
from PIL import Image
im = Image.open("test_images\image1.jpg")
plt.imshow(im, cmap=plt.cm.gray)
plt.show()