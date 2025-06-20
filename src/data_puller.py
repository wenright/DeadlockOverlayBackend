import os
from PIL import Image
import matplotlib.pyplot as plt

from stream import pull_frame
from item_finder import match_item_nn, match_item_hash, crop_item, item_slots_1080p

plt.ion()
f, axarr = plt.subplots(2, 1)
axarr[0].imshow(Image.open("data/empty.png"))
axarr[1].imshow(Image.open("data/empty.png"))

frame, resolution = pull_frame("https://www.twitch.tv/mattercomm")

for i, slot in enumerate(item_slots_1080p):
  item_image = crop_item(frame, resolution, slot, "output/tmp.png")
  item_name = match_item_hash(item_image)

  axarr[0].imshow(item_image)
  axarr[1].imshow(Image.open("data/clean_items/" + item_name + ".png"))
  item_name_fixed = input("Saving as '" + item_name + "', or enter the correct name (s to skip, e to exit): ") or item_name

  if item_name_fixed == "skip" or item_name_fixed == "s":
    continue

  if item_name_fixed == "e":
    break

  # Find a filename that's 1 higher than the current highest
  folder = "data/training_data/" + item_name_fixed + "/"

  if not os.path.exists(folder):
    print("folder doesn't exist, creating " + folder)
    os.makedirs(folder)
  
  current_max = 0
  for entry in os.scandir(folder):
    if ".png" in entry.name:
      current_max = max(current_max, int(entry.name.replace(".png", "")))

  filename = folder + str(current_max + 1) + ".png"
  print("Saving " + filename)
  item_image.save(filename)
