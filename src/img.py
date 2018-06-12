"""
Class for Image
"""
from __future__ import division, print_function, absolute_import
from copy import deepcopy
from PIL import Image
import piexif
from string import upper, lower
from struct import unpack, pack
import os


class Img(object):
    """
    Class for Image
    """
    thumb_size = 360, 360
    EXIF = {'Exif': {}, '0th': {34665: 2110, 40094: ()}, 'Interop': {},
            '1st': {}, 'thumbnail': None, 'GPS': {}}

    def __init__(self, file):
        if self._is_exists(file):
            self.file = file
        else:
            raise NameError(
                "Could not find the file {}\{}".format(os.getcwd(), self.file))
        self.color_names = None
        self.image = self._create_image()
        self.tmb =self._create_thumb()

    def set_color_names(self, color_names):
        """Setter for color names field"""
        self.color_names = color_names
    
    def _is_exists(self, file):
        return os.path.isfile(file)

    def _create_image(self):
        """Opens image"""
        return Image.open(self.file)

    def _create_thumb(self):
        """Creates thumbnail"""
        im = deepcopy(Image.open(self.file))
        im.thumbnail(self.thumb_size, Image.ANTIALIAS)
        return im


    def _create_hashtags(self, h=False, case='', separator=';'):
        """
        h - boolean, set # symbol or not, default - True
        case - string U - upper, L - lower, default - initcap 
        """
        res = ''
        all_color_names = self.color_names
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
        
        im = self.image
        try:
            exif_dict = piexif.load(im.info["exif"])
        except KeyError:
            exif_dict = self.EXIF
        kw_tuple = self._get_exif_keyword_tuple(self._create_hashtags())
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = kw_tuple
        exif_bytes = piexif.dump(exif_dict)
        im.save(self.file, "jpeg", exif=exif_bytes)
