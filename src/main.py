from twitchrealtimehandler import (TwitchImageGrabber)
from PIL import Image
import item_finder
import stream


stream_frame = stream.pull_frame("mikaels1")

image = Image.fromarray(stream_frame)
image.save("../output/full.png")

item_finder.get_items(image)

