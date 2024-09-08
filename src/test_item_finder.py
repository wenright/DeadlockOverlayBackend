import unittest
import item_finder
from PIL import Image

default_resolution = (1920, 1080)

class Test(unittest.TestCase):
  def test_item_finder_simple(self):
    test_frame_0 = Image.open("../data/testing/test_simple.png")
    items = item_finder.get_items(test_frame_0, default_resolution)

    self.assertEqual(items[0], "Headshot Booster")
    self.assertEqual(items[1], "Warp Stone")
    self.assertEqual(items[2], "Mystic Shot")
    self.assertEqual(items[3], "Basic Magazine")

  def test_item_finder_missing_last(self):
    test_frame_empty = Image.open("../data/testing/test_missing_last_slot.png")
    items = item_finder.get_items(test_frame_empty, default_resolution)

    self.assertEqual(items[0], "High Velocity")
    self.assertEqual(items[1], "Hollow Point")
    self.assertEqual(items[2], "Mystic Shot")
    self.assertEqual(items[3], "Empty")

  def test_item_finder_simple(self):
    test_frame_0 = Image.open("../data/testing/test_on_cooldown_1.png")
    items = item_finder.get_items(test_frame_0, default_resolution)

    self.assertEqual(items[0], "Basic Magazine")
    self.assertEqual(items[1], "Point Blank")
    self.assertEqual(items[2], "Slowing Bullets")
    self.assertEqual(items[3], "Fleetfoot")
  
  def test_item_finder_on_cooldown(self):
    test_frame_empty = Image.open("../data/testing/test_on_cooldown_2.png")
    items = item_finder.get_items(test_frame_empty, default_resolution)

    self.assertEqual(items[0], "High Velocity")
    self.assertEqual(items[1], "Monster Rounds")
    self.assertEqual(items[2], "Hollow Point")
    self.assertEqual(items[3], "Mystic Shot")

if __name__ == '__main__':
  unittest.main()