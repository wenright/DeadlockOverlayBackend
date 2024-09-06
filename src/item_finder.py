import imagehash
from PIL import Image
import json

twitch_image = Image.open("../data/twitch_intro.png")

# For orange items at 1080p, might need separate ones for each resolution. 
item_slots = [
  (30, 990, 60, 1020),
  (69, 989, 99, 1020),
  (30, 1028, 60, 1058),
  (69, 1028, 99, 1058)
]

def get_items(image):
    items = []

    with open("../data/items.json") as json_file:
        item_data = json.load(json_file)["orange_items"]
        
        for i, slot in enumerate(item_slots):
            matched_item = match_item(image.crop(slot), item_data)
            items.append(matched_item)
        
        return items

def match_item(item_image, item_data):
    item_image_hash = imagehash.average_hash(item_image)
    min_dist = float("inf")
    min_item = None
    for data in item_data:
        test_image_hash = imagehash.average_hash(Image.open(data["url"]))
        dist = item_image_hash - test_image_hash
        # print(str(data["url"]) + ": " + str(dist))

        if dist < min_dist:
            min_dist = dist
            min_item = data["name"]
    
    empty_dist = item_image_hash - imagehash.average_hash(Image.open("../data/empty.png"))
    if empty_dist < min_dist:
        print("item slot is empty: " + str(empty_dist))
    else:
        print("Closest: " + min_item)

    return min_item
    
