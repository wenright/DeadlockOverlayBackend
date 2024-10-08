from flask import Flask, Response
import redis
import traceback
import re
import json
import os
import keras
import tensorflow as tf
from posthog import Posthog
from dotenv import load_dotenv
from flask_cors import CORS

import stream
import item_finder

load_dotenv()

# Item caching
r = redis.Redis(
  host='redis-15121.c281.us-east-1-2.ec2.redns.redis-cloud.com',
  port=15121,
  db=0,
  password=os.environ.get('REDIS_PASSWORD')
)

# Analytics
posthog = Posthog(
  os.environ.get('POSTHOG_KEY'), 
  host='https://us.i.posthog.com'
)

application = Flask(__name__)
CORS(application)

"""
returns a list of items that the channelName has on screen.
if the channelName exists in the cache, it will use that (15s TTL). 
otherwise pull screenshot from stream, detect items, and return that list of items, as well as set the value in redis
"""
@application.route("/<channelName>", methods=['GET'])
def get_items(channelName):
  posthog.capture(
    channelName, 
    'get_items_api_called'
  )
  
  username_regex = re.compile(r'^[a-zA-Z0-9_]{4,25}$')
  if not username_regex.match(channelName):
    return Response(
      response="Invalid channel name",
      status=400
    )
  
  existing_items = r.get(channelName)
  if existing_items:
    return Response(
      response=existing_items,
      status=200,
      mimetype='application/json'
    )

  try:
    stream_frame, resolution = stream.pull_frame(f'https://www.twitch.tv/{channelName}')

    items = item_finder.get_items(stream_frame, resolution, use_nn=True)

    json_items_string = json.dumps(items)
    r.setex(channelName, 15, json_items_string)

    return Response(
      response=json_items_string,
      status=200,
      mimetype='application/json'
    )
  except Exception:
    print(traceback.format_exc())
  
  return Response(
    response="Failed to retrieve items",
    status=500
  )

if __name__ == "__main__":
  # TODO disable before deployment
  application.debug = True
  application.run()
