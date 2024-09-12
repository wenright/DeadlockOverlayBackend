import unittest
import item_finder
from PIL import Image

default_resolution = (1920, 1080)

class Test(unittest.TestCase):
  # def test_item_finder_simple(self):
  #   test_frame = Image.open("../data/testing/test_simple.png")
  #   items = item_finder.get_items(test_frame, default_resolution)

  #   self.assertEqual(items["orange"][0], "headshot_booster")
  #   self.assertEqual(items["orange"][1], "warp_stone")
  #   self.assertEqual(items["orange"][2], "mystic_shot")
  #   self.assertEqual(items["orange"][3], "basic_magazine")

  #   self.assertEqual(items["green"][0], "bullet_lifesteal")
  #   self.assertEqual(items["green"][1], "sprint_boots")
  #   self.assertEqual(items["green"][2], "enduring_spirit")
  #   self.assertEqual(items["green"][3], "empty")

  #   self.assertEqual(items["purple"][0], "extra_charge")
  #   self.assertEqual(items["purple"][1], "mystic_reach")
  #   self.assertEqual(items["purple"][2], "ethereal_shift")
  #   self.assertEqual(items["purple"][3], "empty")

  #   self.assertEqual(items["flex"][0], "empty")
  #   self.assertEqual(items["flex"][1], "empty")
  #   self.assertEqual(items["flex"][2], "empty")
  #   self.assertEqual(items["flex"][3], "empty")

  # def test_item_finder_missing_last(self):
  #   test_frame_empty = Image.open("../data/testing/test_missing_last_slot.png")
  #   items = item_finder.get_items(test_frame_empty, default_resolution)

  #   self.assertEqual(items["orange"][0], "high_velocity")
  #   self.assertEqual(items["orange"][1], "hollow_point")
  #   self.assertEqual(items["orange"][2], "mystic_shot")
  #   self.assertEqual(items["orange"][3], "empty")

  #   self.assertEqual(items["green"][0], "healing_rite")
  #   self.assertEqual(items["green"][1], "enduring_spirit")
  #   self.assertEqual(items["green"][2], "extra_stamina")
  #   self.assertEqual(items["green"][3], "enchanters_barrier")

  #   self.assertEqual(items["purple"][0], "extra_charge")
  #   self.assertEqual(items["purple"][1], "improved_spirit")
  #   self.assertEqual(items["purple"][2], "superior_cooldown")
  #   self.assertEqual(items["purple"][3], "improved_burst")

  #   self.assertEqual(items["flex"][0], "empty")
  #   self.assertEqual(items["flex"][1], "empty")
  #   self.assertEqual(items["flex"][2], "empty")
  #   self.assertEqual(items["flex"][3], "empty")

  # def test_item_finder_on_cooldown_1(self):
  #   test_frame_empty = Image.open("../data/testing/test_on_cooldown_1.png")
  #   items = item_finder.get_items(test_frame_empty, default_resolution)

  #   self.assertEqual(items["orange"][0], "high_velocity")
  #   self.assertEqual(items["orange"][1], "monster_rounds")
  #   self.assertEqual(items["orange"][2], "hollow_point")
  #   self.assertEqual(items["orange"][3], "mystic_shot")

  #   self.assertEqual(items["green"][0], "enduring_speed")
  #   self.assertEqual(items["green"][1], "superior_stamina")
  #   self.assertEqual(items["green"][2], "healing_booster")
  #   self.assertEqual(items["green"][3], "spirit_lifesteal")

  #   self.assertEqual(items["purple"][0], "cold_front")
  #   self.assertEqual(items["purple"][1], "rapid_recharge")
  #   self.assertEqual(items["purple"][2], "superior_cooldown")
  #   self.assertEqual(items["purple"][3], "improved_burst")

  #   self.assertEqual(items["flex"][0], "empty")
  #   self.assertEqual(items["flex"][1], "empty")
  #   self.assertEqual(items["flex"][2], "empty")
  #   self.assertEqual(items["flex"][3], "empty")

  def test_item_finder_flex_slots(self):
    test_frame = Image.open("../data/testing/test_flex_slots.png")
    items = item_finder.get_items(test_frame, default_resolution, use_nn=True)
    print(items)

    # self.assertEqual(items["orange"][0], "headshot_booster")
    # self.assertEqual(items["orange"][1], "kinetic_dash")
    # self.assertEqual(items["orange"][2], "warp_stone")
    # self.assertEqual(items["orange"][3], "berserker")

    # self.assertEqual(items["green"][0], "sprint_boots")
    # self.assertEqual(items["green"][1], "extra_stamina")
    # self.assertEqual(items["green"][2], "healbane")
    # # self.assertEqual(items["green"][3], "spirit_armor")

    # self.assertEqual(items["purple"][0], "slowing_hex")
    # self.assertEqual(items["purple"][1], "mystic_reach")
    # self.assertEqual(items["purple"][2], "mystic_burst")
    # self.assertEqual(items["purple"][3], "ethereal_shift")

    # self.assertEqual(items["flex"][0], "leech")
    # self.assertEqual(items["flex"][1], "empty")
    # self.assertEqual(items["flex"][2], "bullet_armor")
    # self.assertEqual(items["flex"][3], "healing_barrier")

if __name__ == '__main__':
  unittest.main()