import imagehash
from PIL import Image
import os

# Orange items
item_slots_1080p = {
  "orange": [
    (30, 990, 60, 1020),
    (68, 990, 98, 1020),
    (30, 1028, 60, 1058),
    (68, 1028, 98, 1058)
  ],
  "green": [
    (118, 991, 148, 1021),
    (156, 991, 186, 1021),
    (118, 1029, 148, 1059),
    (156, 1029, 186, 1059)
  ],
  "purple": [
    (205, 991, 235, 1021),
    (243, 991, 273, 1021),
    (205, 1029, 235, 1059),
    (243, 1029, 273, 1059)
  ],
  "flex": [
    (292, 991, 322, 1021),
    (330, 991, 360, 1021),
    (292, 1029, 322, 1059),
    (330, 1029, 360, 1059)
  ]
}

prefix = "../data/items/"

def get_items(image, resolution):
  items = {
    "orange": [],
    "green": [],
    "purple": [],
    "flex": [],
  }
    
  for color, arr in item_slots_1080p.items():
    for i, slot in enumerate(arr):
      file_name = "../output/slot-" + color + "-" + str(i) + ".png"
      cropped_image = crop_item(image, resolution, slot, file_name)

      matched_item = match_item(cropped_image)
      items[color].append(matched_item)
    
  return items

def crop_item(image, resolution, slot, file_name):
  scaled_crop_coordinates = scale_coordinates(slot, (1920, 1080), resolution)
  cropped_image = image.crop(scaled_crop_coordinates)

  if __debug__:
    cropped_image.save(file_name)
  
  return cropped_image

def match_item(item_image):
  item_image_dhash = imagehash.dhash(item_image)
  item_image_phash = imagehash.phash(item_image)
  min_dist = float("inf")
  min_item_filename = ""

  item_images = get_all_item_images()
  
  for image_filename in item_images:
    test_image_dhash = imagehash.dhash(Image.open(prefix + image_filename))
    test_image_phash = imagehash.phash(Image.open(prefix + image_filename))
    dist = (item_image_dhash - test_image_dhash) + (item_image_phash - test_image_phash)
    item_name = image_filename.replace(".png", "")

    if __debug__:
      if dist <= 35:
        print(item_name + ": " + str(dist))

    if dist < min_dist:
      min_dist = dist
      min_item_filename = item_name

  # Check if empty
  print("\n\n")
  empty_dist = imagehash.colorhash(item_image) - imagehash.colorhash(Image.open("../data/empty.png"))
  # print("confidence item slot is empty: " + str(empty_dist))
  if empty_dist == 0:
    print("Slot is empty. Next most likely item: " + min_item_filename)
    return "empty"
  else:
    print("Closest: " + min_item_filename + " (" + str(min_dist) + ")")

  print("\n")

  return min_item_filename

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
  
def get_all_item_images():
  all_item_images = []
  
  for entry in os.scandir(prefix):
    all_item_images.append(entry.name)

  return all_item_images

