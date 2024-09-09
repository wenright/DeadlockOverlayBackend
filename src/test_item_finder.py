import unittest
import item_finder
from PIL import Image

default_resolution = (1920, 1080)

class Test(unittest.TestCase):
  def test_item_finder_simple(self):
    test_frame = Image.open("../data/testing/test_simple.png")
    items = item_finder.get_items(test_frame, default_resolution)

    self.assertEqual(items[0], "headshot_booster")
    self.assertEqual(items[1], "warp_stone")
    self.assertEqual(items[2], "mystic_shot")
    self.assertEqual(items[3], "basic_magazine")

  def test_item_finder_missing_last(self):
    test_frame_empty = Image.open("../data/testing/test_missing_last_slot.png")
    items = item_finder.get_items(test_frame_empty, default_resolution)

    self.assertEqual(items[0], "high_velocity")
    self.assertEqual(items[1], "hollow_point")
    self.assertEqual(items[2], "mystic_shot")
    self.assertEqual(items[3], "Empty")

  def test_item_finder_on_cooldown_1(self):
    test_frame_empty = Image.open("../data/testing/test_on_cooldown_1.png")
    items = item_finder.get_items(test_frame_empty, default_resolution)

    self.assertEqual(items[0], "high_velocity")
    self.assertEqual(items[1], "monster_rounds")
    self.assertEqual(items[2], "hollow_point")
    self.assertEqual(items[3], "mystic_shot")

  def test_item_finder_on_cooldown_2(self):
    test_frame = Image.open("../data/testing/test_on_cooldown_2.png")
    items = item_finder.get_items(test_frame, default_resolution)

    self.assertEqual(items[0], "basic_magazine")
    self.assertEqual(items[1], "point_blank")
    self.assertEqual(items[2], "slowing_bullets")
    self.assertEqual(items[3], "fleetfoot")

if __name__ == '__main__':
  unittest.main()