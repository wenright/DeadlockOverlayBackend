from flask import Flask, Response
import redis
import traceback
import item_finder
import stream
import re
import json

r = redis.Redis(host='redis-15121.c281.us-east-1-2.ec2.redns.redis-cloud.com', port=15121, db=0)

app = Flask(__name__)

"""
returns a list of items if it's already been set.
otherwise read stream, detect items, and return that list of items, as well as set the value in redis
"""
@app.route("/<channelName>")
def get_items(channelName):
  username_regex = re.compile(r'^[a-zA-Z0-9_]{4,25}$')
  if not username_regex.match(channelName):
    return "Invalid channel name"
  
  existing_items = r.get(channelName)
  if existing_items:
    return existing_items

  try:
    stream_frame, resolution = stream.pull_frame(f'https://www.twitch.tv/{channelName}')
    items = item_finder.get_items(stream_frame, resolution)

    json_items_string = json.dumps(items)
    r.setex(channelName, 15, json_items_string)

    return Response(
      response=json_items_string,
      status=200,
      mimetype='application/json'
    )
  except Exception:
    print(traceback.format_exc())
  
  return "Failed to retrieve items"
