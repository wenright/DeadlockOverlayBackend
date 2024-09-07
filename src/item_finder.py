import imagehash
from PIL import Image
import json

twitch_image = Image.open("../data/twitch_intro.png")

# For orange items at 1080p, might need separate ones for each resolution. 
item_slots_1080p = [
  (30, 990, 60, 1020),
  (69, 989, 99, 1020),
  (30, 1028, 60, 1058),
  (69, 1028, 99, 1058)
]

def get_items(image, resolution):
  items = []

  with open("../data/items.json") as json_file:
    item_data = json.load(json_file)["orange_items"]
    
    for i, slot in enumerate(item_slots_1080p):
      scaled_crop_coordinates = scale_coordinates(slot, (1920, 1080), resolution)
      cropped_image = image.crop(scaled_crop_coordinates)

      if __debug__:
        cropped_image.save("../output/slot" + str(i) + ".png")

      matched_item = match_item(cropped_image, item_data)
      items.append(matched_item)
    
  return items

def match_item(item_image, item_data):
  item_image_hash = imagehash.average_hash(item_image)
  min_dist = float("inf")
  min_item_data = None
  for data in item_data:
    test_image_hash = imagehash.average_hash(Image.open(data["url"]))
    dist = item_image_hash - test_image_hash

    if __debug__:
      print(str(data["url"]) + ": " + str(dist))

    if dist < min_dist:
      min_dist = dist
      min_item_data = data

  empty_dist = item_image_hash - imagehash.average_hash(Image.open("../data/empty.png"))
  print("item slot is empty: " + str(empty_dist))
  if empty_dist < min_dist:
    pass
  else:
    print("Closest: " + min_item_data["name"] + " (" + str(min_dist) + ")")

  return min_item_data["name"]

"""
Scale coordinates from an original resolution to a target resolution.

:param coords: List of tuples with coordinates [(x1, y1, x2, y2), ...]
:param original_resolution: Tuple of original width and height (1920, 1080)
:param target_resolution: Tuple of target width and height (new_width, new_height)
:return: List of scaled coordinates
"""
def scale_coordinates(coords, original_resolution, target_resolution):
  original_width, original_height = original_resolution
  target_width, target_height = target_resolution

  x1, y1, x2, y2 = coords

  scaled_x1 = int(x1 * (target_width / original_width))
  scaled_y1 = int(y1 * (target_height / original_height))
  scaled_x2 = int(x2 * (target_width / original_width))
  scaled_y2 = int(y2 * (target_height / original_height))

  return (scaled_x1, scaled_y1, scaled_x2, scaled_y2)

  return scaled_coords
  
