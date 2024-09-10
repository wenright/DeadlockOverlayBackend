import os

from stream import pull_frame
from item_finder import match_item, crop_item, item_slots_1080p

frame, resolution = pull_frame("https://www.twitch.tv/lystic_")

for color, arr in item_slots_1080p.items():
  for i, slot in enumerate(arr):
    item_image = crop_item(frame, resolution, slot, "../output/tmp.png")
    item_name, delta = match_item(item_image)

    # Find a filename that's 1 higher than the current highest
    folder = "../data/real_items/" + item_name + "/"

    if not os.path.exists(folder):
      os.makedirs(folder)
    
    current_max = 0
    for entry in os.scandir(folder):
      current_max = max(current_max, int(entry.name.replace(".png", "")))

    filename = folder + str(current_max + 1) + ".png"
    print("Saving " + filename)
    item_image.save(filename)
