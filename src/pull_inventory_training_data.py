import os
from PIL import Image
import matplotlib.pyplot as plt

from stream import pull_frame
from item_finder import match_item_hash, crop_item, scale_coordinates, item_slots_1080p

plt.ion()
f, axarr = plt.subplots(1, 1)
axarr.imshow(Image.open("data/empty.png"))

frame, resolution = pull_frame("https://www.twitch.tv/mikaels1")

# xmin, ymin, xmax, ymax
bounds = [float('inf'), float('inf'), float('-inf'), float('-inf')]

for color, arr in item_slots_1080p.items():
  for i, slot in enumerate(arr):
    bounds[0] = min(slot[0], bounds[0])
    bounds[1] = min(slot[1], bounds[1])
    bounds[2] = max(slot[2], bounds[2])
    bounds[3] = max(slot[3], bounds[3])

inventory_image = frame.crop(scale_coordinates(bounds, (1920, 1080), resolution))
axarr.imshow(inventory_image)

training_class = (input("Is inventory visible? [Y/n]: ") or 'Y').lower()
folder = "data/inventory_training_data/" + training_class + "/"

if not os.path.exists(folder):
  print("folder doesn't exist, creating " + folder)
  os.makedirs(folder)

current_max = 0
for entry in os.scandir(folder):
  current_max = max(current_max, int(entry.name.replace(".png", "")))

filename = folder + str(current_max + 1) + ".png"
print("Saving " + filename)
inventory_image.save(filename)
