Repo for training an image classifier on Deadlock item icons.

## Running
requires python 3.8

`pip install -r requirements.txt`

`python src/train.py`

also includes some helper scripts like `python src/item_puller.py` which will fetch item screenshots from the stream defined there, then pull up a window with a guess as to what the item is. Just hit enter if it looks right, or type the name if it's wrong. Data will be written to `data/real_items/[item_name]`
