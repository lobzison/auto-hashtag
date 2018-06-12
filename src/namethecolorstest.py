"""
Tests for color extractor module
"""

import unittest
from namethecolors import NameTheColors

class TestColorExtractor(unittest.TestCase):
    """
    Tests for color extractor module
    """
    test_colors_1 = NameTheColors("4.jpg")

    def test_file_not_exists(self):
        self.assertTrue(True)
        with self.assertRaises(NameError):
            NameTheColors('10.jpg')

    def test_colors(self):
        self.assertEquals(set(['Brown', 'Golden Tainoi', 'Neon Carrot',
                               'Gold', 'Dark Orange', 'Orange', 'Yellow', 'Chocolate']),
                          self.test_colors_1.get_color_names())

    def test_hashtags_initcap_hash(self):
        self.assertEquals(
            "#Brown, #Golden Tainoi, #Neon Carrot, #Gold, #Dark Orange, #Orange, #Yellow, #Chocolate, ",
            self.test_colors_1._create_hashtags(separator=', '))

    def test_hashtags_initcap_nohash(self):
        self.assertEquals(
            "Brown, Golden Tainoi, Neon Carrot, Gold, Dark Orange, Orange, Yellow, Chocolate, ",
            self.test_colors_1._create_hashtags(False, separator=', '))

    def test_hashtags_lower_hash(self):
        self.assertEquals(
            "#brown, #golden tainoi, #neon carrot, #gold, #dark orange, #orange, #yellow, #chocolate, ",
            self.test_colors_1._create_hashtags(True, 'L', separator=', '))

    def test_hashtags_upper_hash(self):
        self.assertEquals(
            "#BROWN, #GOLDEN TAINOI, #NEON CARROT, #GOLD, #DARK ORANGE, #ORANGE, #YELLOW, #CHOCOLATE, ",
            self.test_colors_1._create_hashtags(True, 'U', separator=', '))

if __name__ == '__main__':
    unittest.main()

# new = NameTheColors('4.jpg')
# print(new._create_hashtags(True, 'U'))

#brown, #golden tainoi, #neon carrot, #gold, #dark orange, #orange, #yellow, #chocolate,
