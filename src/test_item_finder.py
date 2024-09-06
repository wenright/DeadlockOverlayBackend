import unittest
import item_finder
from PIL import Image

class Test(unittest.TestCase):
  def test_item_finder(self):
    test_frame_0 = Image.open("../data/testing/test0.png")
    items = item_finder.get_items(test_frame_0)

    self.assertEqual(items[0], "Basic Magazine")
    self.assertEqual(items[1], "Point Blank")
    self.assertEqual(items[2], "Slowing Bullets")
    self.assertEqual(items[3], "Fleetfoot")

if __name__ == '__main__':
  unittest.main()