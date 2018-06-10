"""
Tests for color extractor module
"""

import unittest
from namethecolors import NameTheColors

class TestColorExtractor(unittest.TestCase):
    """
    Tests for color extractor module
    """

    def test_file_not_exists(self):
        self.assertTrue(True)
        with self.assertRaises(NameError):
            NameTheColors('10.jpg')

# if __name__ == '__main__':
#     unittest.main()

new = NameTheColors('4.jpg')
print(new.get_color_names())
