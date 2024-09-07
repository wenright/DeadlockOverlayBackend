import traceback
import item_finder
import stream

try:
    stream_frame, resolution = stream.pull_frame("https://www.twitch.tv/averagejonas")

    item_finder.get_items(stream_frame, resolution)
except Exception as exception:
    print(traceback.format_exc())


