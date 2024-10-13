from stream import pull_frame
from item_finder import item_slots_1080p, crop_item

print("Hit enter once the stream is caught up to the item image you're trying to load")
while True:
  item_name = input("Enter item name: ")
  file_name = "data/clean_items/" + item_name + ".png"
  stream_frame, resolution = pull_frame("https://www.twitch.tv/mattercomm")
  cropped_image = crop_item(stream_frame, resolution, item_slots_1080p[0], file_name)

  print(item_name + " saved to " + file_name)
