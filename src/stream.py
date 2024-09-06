import time

# warm up a stream to get past twitch intro 

def pull_frame(channelName):
  image_grabber = TwitchImageGrabber(
    twitch_url="https://www.twitch.tv/" + channelName,
    quality="1080p60",  # quality of the stream could be ["160p", "360p", "480p", "720p", "720p60", "1080p", "1080p60"]
    blocking=True,
    rate=1  # frame per rate (fps)
  )

  frame = image_grabber.grab()
  # print(imagehash.average_hash(Image.fromarray(frame)) - imagehash.average_hash(twitch_image))
  # while imagehash.average_hash(Image.fromarray(frame).convert("L")) - imagehash.average_hash(twitch_image) < 70:
  #     print(imagehash.average_hash(Image.fromarray(frame).convert("L")) - imagehash.average_hash(twitch_image))
  #     frame = image_grabber.grab()
  #     # Image.fromarray(frame).convert("L").show()
  #     # twitch_image.convert("L").show()
  #     time.sleep(1)
  for i in range(20):
      print("grabs")
      frame = image_grabber.grab()
  image_grabber.terminate()  # stop the transcoding

  return frame
