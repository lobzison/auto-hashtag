"""
Module for genereting hashtagf for a photo
"""

from namethecolors import NameTheColors
import os

class AutoHashtag(object):
    """
    Class for generating hashtag
    """

    @staticmethod
    def get_hashtag_set(photo):
        """
        photo: String with file location
        returns python set of hashtags
        """
        p = NameTheColors(photo)
        h = p.get_color_names()
        p._delete_thumb()
        return h

    @staticmethod
    def set_hashtags(photo):
        """
        photo: String with file location
        Sets hashtags to photo's EXIF
        """
        p = NameTheColors(photo)
        p._set_hashtags()
        p._delete_thumb()

    @staticmethod
    def set_folder_hashtags(folder):
        """
        folder: String with folder location
        Sets hashtags for all photos in the folder
        """
        if os.path.isdir(folder):
            for filename in os.listdir(folder):
                if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
                    AutoHashtag.set_hashtags(os.path.join(folder, filename))
        else:
            print("input is not a folder {}".format(folder))     
        
