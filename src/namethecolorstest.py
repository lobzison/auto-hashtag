"""
Tests for color extractor module
"""

import unittest
from namethecolors import NameTheColors
from img import Img

class TestColorExtractor(unittest.TestCase):
    """
    Tests for color extractor module
    """
    ntc = NameTheColors()
    test_colors_1 = Img("4.jpg")
    test_colors_1.set_color_names(ntc._get_color_names(test_colors_1))


    def test_file_not_exists(self):
        self.assertTrue(True)
        with self.assertRaises(NameError):
            Img('10.jpg')

    def test_colors(self):
        self.assertEquals(set(['Brown', 'Gold Drop', 'Neon Carrot',
                               'Gold', 'Dark Orange', 'Orange', 'Yellow', 'Chocolate']),
                          self.test_colors_1.color_names)

    def test_hashtags_initcap_hash(self):
        self.assertEquals(
            "#Brown;#Gold Drop;#Neon Carrot;#Gold;#Dark Orange;#Orange;#Yellow;#Chocolate",
            self.test_colors_1._create_hashtags(True))

    def test_hashtags_initcap_nohash(self):
        self.assertEquals(
            "Brown;Gold Drop;Neon Carrot;Gold;Dark Orange;Orange;Yellow;Chocolate",
            self.test_colors_1._create_hashtags(False))

    def test_hashtags_lower_hash(self):
        self.assertEquals(
            "#brown;#gold drop;#neon carrot;#gold;#dark orange;#orange;#yellow;#chocolate",
            self.test_colors_1._create_hashtags(True, 'L'))

    def test_hashtags_upper_hash(self):
        self.assertEquals(
            "#BROWN;#GOLD DROP;#NEON CARROT;#GOLD;#DARK ORANGE;#ORANGE;#YELLOW;#CHOCOLATE",
            self.test_colors_1._create_hashtags(True, 'U'))

if __name__ == '__main__':
    unittest.main()

# new = NameTheColors('4.jpg')
# print(new._create_hashtags(True, 'U'))

#brown, #golden tainoi, #neon carrot, #gold, #dark orange, #orange, #yellow, #chocolate,
'#BROWN;#GOLD DROP;#NEON CARROT;#GOLD;#DARK ORANGE;#ORANGE;#YELLOW;#CHOCOLATE'
'#BROWN;#GOLDEN TAINOI;#NEON CARROT;#GOLD;#DARK ORANGE;#ORANGE;#YELLOW;#CHOCOLATE'
