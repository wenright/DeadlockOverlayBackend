from stream import pull_frame
from item_finder import item_slots_1080p, crop_item
from PIL import Image
import matplotlib.pyplot as plt

plt.ion()
f, axarr = plt.subplots(1, 1)
axarr.imshow(Image.open("data/empty.png"))

input("Hit enter once the stream is caught up to the item image you're trying to load...")

stream_frame, resolution = pull_frame("https://www.twitch.tv/mattercomm")
idx = 0

while idx < len(item_slots_1080p):
  cropped_image = crop_item(stream_frame, resolution, item_slots_1080p[idx], None)
  axarr.imshow(cropped_image)
  item_name = input("Enter item name: ")

  if not item_name:
    print("Empty input, exiting")
    break
  
  file_name = "data/clean_items/" + item_name + ".png"
  cropped_image.save(file_name)

  print(item_name + " saved to " + file_name)
  idx += 1

print("Done")
