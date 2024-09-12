import imagehash
from PIL import Image
import os
import numpy as np
import tensorflow as tf
import keras

item_slots_1080p = {
  "orange": [
    (30, 991, 60, 1021),
    (68, 991, 98, 1021),
    (30, 1029, 60, 1059),
    (68, 1029, 98, 1059)
  ],
  "green": [
    (117, 991, 147, 1021),
    (155, 991, 185, 1021),
    (117, 1029, 147, 1059),
    (155, 1029, 185, 1059)
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

prefix = "../data/clean_items/"

# Load Keras model
model = keras.models.load_model("../data/models/item_classifier.keras")
class_names = np.load("../data/models/class_names.npy")

def get_items(image, resolution, use_nn=False):
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
      
      # print("\n-- " + color + " " + str(i) + " --")
      matched_item = None
      if use_nn:
        matched_item = match_item_nn(cropped_image)
      else:
        matched_item = match_item_hash(cropped_image)

      items[color].append(matched_item)
    
  return items

def crop_item(image, resolution, slot, file_name=None):
  scaled_crop_coordinates = scale_coordinates(slot, (1920, 1080), resolution)
  cropped_image = image.crop(scaled_crop_coordinates).resize((30, 30))

  if __debug__ and file_name:
    cropped_image.save(file_name)
  
  return cropped_image

def match_item_nn(item_image):
  img_array = tf.keras.utils.img_to_array(item_image)
  img_array = tf.expand_dims(img_array, 0) # Create a batch
  predictions = model.predict(img_array)
  score = tf.nn.softmax(predictions[0])
  print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
  )

def match_item_hash(item_image):
  item_image_dhash = imagehash.dhash(item_image)
  item_image_phash = imagehash.phash(item_image)
  item_image_colorhash = imagehash.colorhash(item_image)
  min_dist = float("inf")
  min_item_filename = ""

  item_images = get_all_item_images()
  
  for image_filename in item_images:
    test_image_dhash = imagehash.dhash(Image.open(prefix + image_filename))
    test_image_phash = imagehash.phash(Image.open(prefix + image_filename))
    test_image_colorhash = imagehash.colorhash(Image.open(prefix + image_filename))
    dist = (item_image_dhash - test_image_dhash) + (item_image_phash - test_image_phash)
    dist += (item_image_colorhash - test_image_colorhash) * 4
    item_name = image_filename.replace(".png", "")

    # if __debug__:
    #   if dist <= 60:
    #     print(item_name + ": " + str(item_image_dhash - test_image_dhash) + ", " + str(item_image_phash - test_image_phash) + ", " + str((item_image_colorhash - test_image_colorhash) * 4) + " = " + str(dist))

    if dist < min_dist:
      min_dist = dist
      min_item_filename = item_name

  # Check if empty
  empty_dist = imagehash.colorhash(item_image) - imagehash.colorhash(Image.open("../data/empty.png"))
  # print("confidence item slot is empty: " + str(empty_dist))
  if empty_dist <= 3 or min_dist >= 50:
    # print("Slot is empty. Next most likely item: " + min_item_filename)
    return "empty"
  else:
    # print("Closest: " + min_item_filename + " (" + str(min_dist) + ")")
    pass

  # print("\n")

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

