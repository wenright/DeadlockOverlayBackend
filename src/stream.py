import cv2
import numpy as np
import streamlink
from PIL import Image

# warm up a stream to get past twitch intro 

def pull_frame(stream_url):
  # Get the stream URL using streamlink
  streams = streamlink.streams(stream_url)
  if 'best' not in streams:
    raise Exception("Unable to find the best quality stream.")
  
  # Get the best stream URL
  stream = streams['best']
  stream_url = stream.url

  # Open the video capture using OpenCV
  cap = cv2.VideoCapture(stream_url)

  # Check if the stream opened successfully
  if not cap.isOpened():
    raise Exception("Failed to open stream.")

  resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

  # Read a frame from the stream
  ret, frame = cap.read()

  # Release the video capture object
  cap.release()

  if ret:
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    converted_image = Image.fromarray(frame_rgb)
    converted_image.save("../output/full.png")

    return converted_image, resolution
  else:
    raise Exception("Failed to capture a frame.")

