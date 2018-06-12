"""
Module for genereting hashtagf for a photo
"""

from namethecolors import NameTheColors
from img import Img
import os


class AutoHashtag(object):
    """
    Class for generating hashtag
    """
    ntc = NameTheColors()

    def get_hashtag_set(self, photo):
        """
        photo: String with file location
        returns python set of hashtags
        """
        im = Img(photo)
        colors = self.ntc._get_color_names(im)
        im.set_color_names(colors)
        return im._create_hashtags()

    def set_hashtags(self, photo):
        """
        photo: String with file location
        Sets hashtags to photo's EXIF
        """
        im = Img(photo)
        colors = self.ntc._get_color_names(im)
        im.set_color_names(colors)
        im._set_hashtags()

    def set_folder_hashtags(self, folder):
        """
        folder: String with folder location
        Sets hashtags for all photos in the folder
        """
        if os.path.isdir(folder):
            for filename in os.listdir(folder):
                if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
                    self.set_hashtags(os.path.join(folder, filename))
        else:
            print("input is not a folder {}".format(folder))
